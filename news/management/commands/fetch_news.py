import feedparser
import urllib.request
import ssl
import re
import logging
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from news.models import Story
from news.sources_config import LANGUAGE_FEEDS

logger = logging.getLogger('news.fetch')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('fetch_news.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


class Command(BaseCommand):
    help = 'Fetch latest news from wire services'

    def add_arguments(self, parser):
        parser.add_argument(
            '--language',
            type=str,
            default='all',
            choices=['all', 'en', 'es'],
            help='Language to fetch (all, en, es)'
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

    def get_meta_description(self, url):
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')
                
                # Try meta description
                match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', html, re.I)
                if not match:
                    match = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']', html, re.I)
                
                if match:
                    desc = match.group(1).strip()
                    # Clean up HTML entities
                    desc = desc.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
                    return desc[:500]
                
                # Try og:description
                match = re.search(r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']+)["\']', html, re.I)
                if match:
                    return match.group(1).strip()[:500]
                    
        except Exception:
            pass
        return ''

    def fetch_language(self, language):
        feeds = LANGUAGE_FEEDS.get(language, [])
        logger.info(f'Fetching {language} news from {len(feeds)} sources')
        self.stdout.write(f"\nFetching {language} news...")
        
        cutoff = timezone.now() - timedelta(hours=24)
        seen_urls = set(Story.objects.filter(language=language).values_list('url', flat=True))
        total_new = 0
        total_dupes = 0
        meta_fetched = 0
        
        for source_name, feed_url in feeds:
            self.stdout.write(f"  {source_name}...", ending=" ")
            logger.info(f'Fetching {source_name} ({language})')
            
            feed = self.fetch_feed(feed_url)
            
            if not feed.entries:
                logger.warning(f'{source_name}: EMPTY')
                self.stdout.write(self.style.WARNING("EMPTY"))
                continue
            
            source_count = 0
            for entry in feed.entries[:50]:
                if entry.get('link') in seen_urls:
                    total_dupes += 1
                    continue
                
                published = entry.get('published_parsed') or entry.get('updated_parsed')
                if published:
                    pub_time = timezone.make_aware(datetime(*published[:6]))
                else:
                    pub_time = timezone.now()

                if pub_time < cutoff:
                    continue

                rss_excerpt = entry.get('summary', '')[:800]
                meta_desc = self.get_meta_description(entry.link)
                
                title_words = set(entry.title.lower().split())
                if rss_excerpt:
                    rss_words = set(rss_excerpt.lower().split())
                    overlap = len(title_words & rss_words) / len(title_words) if title_words else 0
                    use_rss = overlap < 0.7 and len(rss_excerpt) > 50
                else:
                    use_rss = False
                
                if meta_desc and not use_rss:
                    excerpt = meta_desc
                    meta_fetched += 1
                else:
                    excerpt = rss_excerpt

                try:
                    if not Story.objects.filter(url=entry.link).exists():
                        Story.objects.create(
                            title=entry.title[:500],
                            excerpt=excerpt,
                            url=entry.link,
                            source=source_name,
                            language=language,
                            category='world',
                            published=pub_time,
                        )
                        seen_urls.add(entry.link)
                        total_new += 1
                        source_count += 1
                    else:
                        total_dupes += 1
                except Exception as e:
                    logger.error(f'Error creating story: {e}')
            
            logger.info(f'{source_name}: {source_count} stories')
            self.stdout.write(f"OK ({source_count} new)")
        
        return total_new, total_dupes, meta_fetched

    def handle(self, *args, **options):
        language = options['language']
        logger.info(f'Starting news fetch (language: {language})')
        
        cutoff = timezone.now() - timedelta(hours=24)
        
        deleted = Story.objects.filter(published__lt=cutoff).delete()
        logger.info(f'Cleaned old stories: {deleted[0]} removed')
        self.stdout.write(f"Cleaned old stories: {deleted[0]} removed")
        
        total_new = 0
        total_dupes = 0
        meta_fetched = 0
        
        if language == 'all':
            languages = LANGUAGE_FEEDS.keys()
        else:
            languages = [language]
        
        for lang in languages:
            new, dupes, meta = self.fetch_language(lang)
            total_new += new
            total_dupes += dupes
            meta_fetched += meta
        
        logger.info(f'Fetch complete: {total_new} new, {total_dupes} dupes, {meta_fetched} meta')
        self.stdout.write(self.style.SUCCESS(f"\nFetch complete: {total_new} new stories ({total_dupes} duplicates skipped, {meta_fetched} with meta descriptions)"))
