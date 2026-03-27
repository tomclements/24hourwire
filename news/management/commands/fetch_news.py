import feedparser
import urllib.request
import ssl
import re
import logging
from datetime import datetime, timedelta
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
            with urllib.request.urlopen(req, context=ctx, timeout=20) as response:
                return feedparser.parse(response.read())
        except Exception:
            try:
                return feedparser.parse(url)
            except Exception:
                return feedparser.parse('')

    def fetch_language(self, language):
        feeds = LANGUAGE_FEEDS.get(language, [])
        logger.info(f'Fetching {language} news from {len(feeds)} sources')
        self.safe_write(f"\nFetching {language} news...")

        cutoff = timezone.now() - timedelta(hours=24)

        # Load existing hashes for this language — two queries instead of N
        existing_url_hashes = set(
            Story.objects.filter(language=language)
            .values_list('url_hash', flat=True)
        )
        existing_source_fps = set(
            Story.objects.filter(language=language, url_hash__gt='')
            .values_list('source', 'title_fingerprint')
        )

        total_new = 0
        total_dupes = 0
        url_dupes = 0
        title_dupes = 0
        to_create = []

        for source_name, feed_url in feeds:
            self.safe_write(f"  {source_name}...", ending=" ")
            logger.info(f'Fetching {source_name} ({language})')

            feed = self.fetch_feed(feed_url)

            if not feed.entries:
                logger.warning(f'{source_name}: EMPTY')
                self.safe_write(self.style.WARNING("EMPTY"))
                continue

            source_count = 0
            for entry in feed.entries[:50]:
                url = normalize_url(entry.get('link', ''))
                import hashlib
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

                rss_excerpt = entry.get('summary', '')[:800]

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
                existing_url_hashes.add(url_hash)
                existing_source_fps.add((source_name, fp))
                total_new += 1
                source_count += 1

            logger.info(f'{source_name}: {source_count} stories')
            self.safe_write(f"OK ({source_count} new)")

        # Bulk insert — single DB round-trip
        if to_create:
            Story.objects.bulk_create(to_create, ignore_conflicts=True)

        return total_new, total_dupes, url_dupes, title_dupes

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

        if language == 'all':
            languages = LANGUAGE_FEEDS.keys()
        else:
            languages = [language]

        for lang in languages:
            new, dupes, u_dupes, t_dupes = self.fetch_language(lang)
            total_new += new
            total_dupes += dupes
            url_dupes += u_dupes
            title_dupes += t_dupes

        # Build story clusters for "Most Covered" tab
        for lang in languages:
            cluster_count = build_clusters(lang)
            self.safe_write(f"Built {cluster_count} clusters for {lang}")

        logger.info(f'Fetch complete: {total_new} new, {total_dupes} dupes ({url_dupes} url, {title_dupes} title)')
        self.safe_write(self.style.SUCCESS(
            f"\nFetch complete: {total_new} new stories "
            f"({total_dupes} duplicates skipped: {url_dupes} url, {title_dupes} title)"
        ))
