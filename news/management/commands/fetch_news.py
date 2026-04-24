import feedparser
import urllib.request
import ssl
import re
import logging
import hashlib
import gc
import time
from datetime import datetime, timedelta
from difflib import SequenceMatcher
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import OperationalError, connection
from news.models import Story, normalize_url, title_fingerprint
from news.sources_config import LANGUAGE_FEEDS, SUPPORTED_LANGUAGES
from news.categorization import categorize_story


# Pre-compile regex patterns for efficiency
GOOGLE_NEWS_URL_PATTERN = re.compile(r'<a\s+href="https?://news\.google\.com/rss/articles/[^"]*"[^>]*>.*?</a>', re.IGNORECASE | re.DOTALL)
HTML_TAG_PATTERN = re.compile(r'<[^>]+>')
URL_PATTERN = re.compile(r'https?://\S+')
WHITESPACE_PATTERN = re.compile(r'\s+')

# Setup logger first
logger = logging.getLogger('news.fetch')
logger.setLevel(logging.INFO)
# Use UTF-8 encoding to handle international characters (Arabic, Cyrillic, Chinese, etc.)
handler = logging.FileHandler('fetch_news.log', encoding='utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


def extract_image_url(entry):
    """Extract the best image URL from a feedparser entry.
    
    Checks multiple RSS image formats in order of preference:
    1. media_thumbnail (most common for news feeds)
    2. media_content with medium='image'
    3. enclosures with image type
    4. First <img> tag in summary/content
    
    Returns empty string if no image found.
    """
    # media:thumbnail is most common for news feeds (BBC, Reuters, etc.)
    thumbnails = entry.get('media_thumbnail', [])
    if thumbnails:
        # thumbnails is a list of dicts with 'url', 'width', 'height'
        # Pick the largest one if multiple sizes available
        best = max(thumbnails, key=lambda t: int(t.get('width', 0)) * int(t.get('height', 0)))
        return best.get('url', '')
    
    # media:content with medium='image'
    media_content = entry.get('media_content', [])
    for media in media_content:
        if media.get('medium') == 'image' and media.get('url'):
            return media['url']
    
    # enclosures
    enclosures = entry.get('enclosures', [])
    for enc in enclosures:
        if enc.get('type', '').startswith('image/'):
            return enc.get('href', '')
    
    # Try to extract from HTML in summary or content
    html_content = entry.get('summary', '') or entry.get('content', [{}])[0].get('value', '')
    if html_content:
        # Look for <img> tags
        img_match = re.search(r'<img[^>]+src\s*=\s*["\'](https?://[^"\']+)["\']', html_content, re.IGNORECASE)
        if img_match:
            return img_match.group(1)
    
    return ''


def retry_on_db_error(max_retries=3, delay=1):
    """Decorator to retry database operations on connection errors."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except OperationalError as e:
                    last_error = e
                    logger.warning(f'Database connection error (attempt {attempt + 1}/{max_retries}): {e}')
                    if attempt < max_retries - 1:
                        time.sleep(delay)  # Fixed 1s delay, not exponential
                        # Try to reconnect
                        try:
                            connection.close()
                        except Exception:
                            pass
                    else:
                        raise last_error
            return None
        return wrapper
    return decorator


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
            # Don't use feedparser.parse(url) directly as it has no timeout
            # Return empty feed instead to prevent hanging
            return feedparser.parse('')

    def title_similarity(self, title1, title2):
        """Calculate similarity ratio between two titles."""
        return SequenceMatcher(None, title1.lower(), title2.lower()).ratio()

    def load_existing_hashes_with_retry(self, language, recent_cutoff, max_retries=2):
        """Load existing URL hashes with retry logic for database connection issues."""
        for attempt in range(max_retries):
            try:
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
                
                return existing_url_hashes, existing_source_fps
            except OperationalError as e:
                logger.warning(f'Database connection error loading hashes (attempt {attempt + 1}/{max_retries}): {e}')
                if attempt < max_retries - 1:
                    time.sleep(1)  # Fixed 1s delay
                    try:
                        connection.close()
                    except Exception:
                        pass
                else:
                    logger.error(f'Failed to load hashes after {max_retries} attempts - continuing with empty sets')
                    # Return empty sets instead of crashing - allows fetch to continue
                    return set(), set()
        return set(), set()

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
        
        # Load URL hashes with retry logic
        existing_url_hashes, existing_source_fps = self.load_existing_hashes_with_retry(language, recent_cutoff)
        
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
            # Safe encoding for Windows console
            safe_name = source_name.encode('ascii', 'replace').decode('ascii')
            self.safe_write(f"  {safe_name}...", ending=" ")
            logger.info(f'Fetching {safe_name} ({language})')

            feed = self.fetch_feed(feed_url)

            if not feed.entries:
                logger.warning(f'{safe_name}: EMPTY')
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

                # Create excerpt - clean HTML and Google News reference URLs
                rss_excerpt = entry.get('summary', '')[:500]  # Reduced from 800
                
                # Clean Google News RSS reference URLs immediately
                rss_excerpt = GOOGLE_NEWS_URL_PATTERN.sub(' ', rss_excerpt)
                # Remove all HTML tags
                rss_excerpt = HTML_TAG_PATTERN.sub(' ', rss_excerpt)
                # Remove leftover URLs
                rss_excerpt = URL_PATTERN.sub(' ', rss_excerpt)
                # Clean up whitespace
                rss_excerpt = WHITESPACE_PATTERN.sub(' ', rss_excerpt).strip()
                
                title_words = set(title.lower().split())
                if rss_excerpt:
                    rss_words = set(rss_excerpt.lower().split())
                    overlap = len(title_words & rss_words) / len(title_words) if title_words else 0
                    excerpt = rss_excerpt if overlap < 0.7 and len(rss_excerpt) > 50 else ''
                else:
                    excerpt = ''

                # Extract image URL from RSS entry
                image_url = extract_image_url(entry)

                to_create.append(Story(
                    source=source_name,
                    title=title,
                    excerpt=excerpt,
                    url=entry.link,
                    url_hash=url_hash,
                    title_fingerprint=fp,
                    language=language,
                    category=categorize_story(title, language),
                    published=pub_time,
                    image_url=image_url,
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

            # Safe logging for Unicode source names
            try:
                logger.info(f'{source_name}: {source_count} stories')
            except UnicodeEncodeError:
                safe_name = source_name.encode('ascii', 'replace').decode('ascii')
                logger.info(f'{safe_name}: {source_count} stories')
            self.safe_write(f"OK ({source_count} new)")
            
            # Force garbage collection after each source to prevent memory buildup
            if len(recent_source_stories) > 100:
                recent_source_stories.clear()
                gc.collect()

        return total_new, total_dupes, url_dupes, title_dupes, fuzzy_dupes

    @retry_on_db_error(max_retries=3, delay=2)
    def clean_old_stories(self):
        """Clean stories older than 24 hours with retry logic."""
        cutoff = timezone.now() - timedelta(hours=24)
        deleted = Story.objects.filter(published__lt=cutoff).delete()
        return deleted[0]

    def check_db_connection(self, max_retries=3):
        """Check if database connection is working."""
        for attempt in range(max_retries):
            try:
                # Try a simple query - use a timeout to prevent hanging
                Story.objects.first()
                return True
            except OperationalError as e:
                logger.warning(f'Database connection check failed (attempt {attempt + 1}/{max_retries}): {e}')
                if attempt < max_retries - 1:
                    time.sleep(1)  # Fixed 1s delay
                    try:
                        connection.close()
                    except Exception:
                        pass
                else:
                    return False
            except Exception as e:
                # Log other errors but don't retry
                logger.error(f'Unexpected error checking DB connection: {e}')
                return False
        return False

    def handle(self, *args, **options):
        language = options['language']
        logger.info(f'Starting news fetch (language: {language})')

        # Check database connection before starting
        if not self.check_db_connection():
            logger.error('Database connection failed - cannot proceed with fetch')
            self.safe_write(self.style.ERROR("ERROR: Database connection failed. Cannot fetch news."))
            return

        try:
            deleted_count = self.clean_old_stories()
            logger.info(f'Cleaned old stories: {deleted_count} removed')
            self.safe_write(f"Cleaned old stories: {deleted_count} removed")
        except Exception as e:
            logger.error(f'Failed to clean old stories: {e}')
            self.safe_write(self.style.WARNING(f"Warning: Could not clean old stories: {e}"))

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

        # Clear cache so fresh stories appear immediately
        if total_new > 0:
            from django.core.cache import cache
            cache.clear()
            logger.info('Cache cleared after fetch')
            self.safe_write(self.style.SUCCESS("Cache cleared"))

        logger.info(f'Fetch complete: {total_new} new, {total_dupes} dupes ({url_dupes} url, {title_dupes} title, {fuzzy_dupes} fuzzy)')
        self.safe_write(self.style.SUCCESS(
            f"\nFetch complete: {total_new} new stories "
            f"({total_dupes} duplicates skipped: {url_dupes} url, {title_dupes} title, {fuzzy_dupes} similar)"
        ))