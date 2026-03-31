import feedparser
import urllib.request
import ssl
import re
import logging
import hashlib
import gc
from datetime import datetime, timedelta
from difflib import SequenceMatcher
from django.core.management.base import BaseCommand
from django.utils import timezone
from news.models import Story, normalize_url, title_fingerprint, build_clusters
from news.sources_config import LANGUAGE_FEEDS, SUPPORTED_LANGUAGES

logger = logging.getLogger('news.fetch')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('fetch_news.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


class Command(BaseCommand):
    help = 'Fetch latest news from wire services'

    def safe_write(self, msg, **kwargs):
        """Write to stdout, falling back to ASCII-safe version on encoding errors."""
        try:
            self.stdout.write(msg, **kwargs)
        except UnicodeEncodeError:
            self.stdout.write(msg.encode('ascii', 'replace').decode('ascii'), **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            '--language',
            type=str,
            default='all',
            choices=['all'] + sorted(SUPPORTED_LANGUAGES),
            help=f'Language to fetch (all, {", ".join(sorted(SUPPORTED_LANGUAGES))})'
        )

    def fetch_feed(self, url):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
                return feedparser.parse(response.read())
        except Exception:
            try:
                return feedparser.parse(url)
            except Exception:
                return feedparser.parse('')

    def title_similarity(self, title1, title2):
        """Calculate similarity ratio between two titles."""
        return SequenceMatcher(None, title1.lower(), title2.lower()).ratio()

    def fetch_language(self, language):
        feeds = LANGUAGE_FEEDS.get(language, [])
        logger.info(f'Fetching {language} news from {len(feeds)} sources')
        self.safe_write(f"\nFetching {language} news...")

        cutoff = timezone.now() - timedelta(hours=24)

        # OPTIMIZATION: Only load hashes for last 6 hours to save memory
        # Stories older than 24h get deleted anyway, so we only need recent ones
        recent_cutoff = timezone.now() - timedelta(hours=6)
        
        logger.info(f'Loading existing hashes for {language}...')
        self.safe_write(f"  Loading existing hashes...", ending=" ")
        
        # Load URL hashes (only recent ones to save memory)
        existing_url_hashes = set(
            Story.objects.filter(language=language, published__gte=recent_cutoff)
            .values_list('url_hash', flat=True)
        )
        
        # Load source+fingerprint combos (only recent ones)
        existing_source_fps = set(
            Story.objects.filter(language=language, published__gte=recent_cutoff)
            .values_list('source', 'title_fingerprint')
        )
        
        self.safe_write(f"OK ({len(existing_url_hashes)} hashes, {len(existing_source_fps)} fingerprints)")
        logger.info(f'Loaded {len(existing_url_hashes)} URL hashes, {len(existing_source_fps)} fingerprints')

        total_new = 0
        total_dupes = 0
        url_dupes = 0
        title_dupes = 0
        fuzzy_dupes = 0
        
        # Track recent stories per source for fuzzy deduplication
        recent_source_stories = {}

        for source_name, feed_url in feeds:
            self.safe_write(f"  {source_name}...", ending=" ")
            logger.info(f'Fetching {source_name} ({language})')

            feed = self.fetch_feed(feed_url)

            if not feed.entries:
                logger.warning(f'{source_name}: EMPTY')
                self.safe_write(self.style.WARNING("EMPTY"))
                continue

            source_count = 0
            to_create = []
            
            for entry in feed.entries[:25]:  # Reduced from 30 to save memory/processing
                url = normalize_url(entry.get('link', ''))
                url_hash = hashlib.sha256(url.encode()).hexdigest()

                # Level 1: Skip if normalized URL already stored
                if url_hash in existing_url_hashes:
                    url_dupes += 1
                    total_dupes += 1
                    continue

                published = entry.get('published_parsed') or entry.get('updated_parsed')
                if published:
                    pub_time = timezone.make_aware(datetime(*published[:6]))
                else:
                    pub_time = timezone.now()

                if pub_time < cutoff:
                    continue

                # Handle title encoding
                try:
                    title = entry.title[:500].encode('utf-8', 'ignore').decode('utf-8')
                except Exception:
                    title = str(entry.title[:500])

                fp = title_fingerprint(title)

                # Level 2: Skip if same source already has this title fingerprint
                if (source_name, fp) in existing_source_fps:
                    title_dupes += 1
                    total_dupes += 1
                    continue

                # Level 3: Fuzzy deduplication
                is_fuzzy_dup = False
                if source_name in recent_source_stories:
                    for recent_title, recent_time in recent_source_stories[source_name][-5:]:  # Only check last 5
                        time_diff = (pub_time - recent_time).total_seconds() / 60
                        if time_diff <= 30:
                            similarity = self.title_similarity(title, recent_title)
                            if similarity >= 0.75:
                                is_fuzzy_dup = True
                                break
                
                if is_fuzzy_dup:
                    fuzzy_dupes += 1
                    total_dupes += 1
                    continue

                # Create excerpt
                rss_excerpt = entry.get('summary', '')[:500]  # Reduced from 800
                title_words = set(title.lower().split())
                if rss_excerpt:
                    rss_words = set(rss_excerpt.lower().split())
                    overlap = len(title_words & rss_words) / len(title_words) if title_words else 0
                    excerpt = rss_excerpt if overlap < 0.7 and len(rss_excerpt) > 50 else ''
                else:
                    excerpt = ''

                to_create.append(Story(
                    source=source_name,
                    title=title,
                    excerpt=excerpt,
                    url=entry.link,
                    url_hash=url_hash,
                    title_fingerprint=fp,
                    language=language,
                    category='world',
                    published=pub_time,
                ))
                
                # Track for fuzzy deduplication
                if source_name not in recent_source_stories:
                    recent_source_stories[source_name] = []
                recent_source_stories[source_name].append((title, pub_time))
                recent_source_stories[source_name] = recent_source_stories[source_name][-10:]  # Keep only last 10
                
                # Add to existing sets to prevent duplicates within this run
                existing_url_hashes.add(url_hash)
                existing_source_fps.add((source_name, fp))
                
                total_new += 1
                source_count += 1
                
                # Insert in batches
                if len(to_create) >= 25:
                    Story.objects.bulk_create(to_create, ignore_conflicts=True)
                    to_create = []

            # Insert remaining stories for this source
            if to_create:
                Story.objects.bulk_create(to_create, ignore_conflicts=True)

            logger.info(f'{source_name}: {source_count} stories')
            self.safe_write(f"OK ({source_count} new)")
            
            # Force garbage collection after each source to prevent memory buildup
            if len(recent_source_stories) > 100:
                recent_source_stories.clear()
                gc.collect()

        return total_new, total_dupes, url_dupes, title_dupes, fuzzy_dupes

    def handle(self, *args, **options):
        language = options['language']
        logger.info(f'Starting news fetch (language: {language})')

        cutoff = timezone.now() - timedelta(hours=24)

        deleted = Story.objects.filter(published__lt=cutoff).delete()
        logger.info(f'Cleaned old stories: {deleted[0]} removed')
        self.safe_write(f"Cleaned old stories: {deleted[0]} removed")

        total_new = 0
        total_dupes = 0
        url_dupes = 0
        title_dupes = 0
        fuzzy_dupes = 0

        if language == 'all':
            languages = list(LANGUAGE_FEEDS.keys())
        else:
            languages = [language]

        for lang in languages:
            new, dupes, u_dupes, t_dupes, f_dupes = self.fetch_language(lang)
            total_new += new
            total_dupes += dupes
            url_dupes += u_dupes
            title_dupes += t_dupes
            fuzzy_dupes += f_dupes
            
            # Force garbage collection between languages
            gc.collect()

        # Build story clusters for "Most Covered" tab
        # Only build if not too many stories to prevent memory issues
        if total_new < 2000:
            for lang in languages:
                try:
                    cluster_count = build_clusters(lang, max_stories=500)
                    self.safe_write(f"Built {cluster_count} clusters for {lang}")
                except Exception as e:
                    logger.error(f'Error building clusters for {lang}: {e}')
        else:
            self.safe_write(self.style.WARNING(
                f"Skipping cluster build: {total_new} new stories (too many for memory)"
            ))

        logger.info(f'Fetch complete: {total_new} new, {total_dupes} dupes ({url_dupes} url, {title_dupes} title, {fuzzy_dupes} fuzzy)')
        self.safe_write(self.style.SUCCESS(
            f"\nFetch complete: {total_new} new stories "
            f"({total_dupes} duplicates skipped: {url_dupes} url, {title_dupes} title, {fuzzy_dupes} similar)"
        ))