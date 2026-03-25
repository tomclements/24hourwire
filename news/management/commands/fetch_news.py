import feedparser
import urllib.request
import ssl
import re
import logging
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from news.models import Story

logger = logging.getLogger('news.fetch')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('fetch_news.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


class Command(BaseCommand):
    help = 'Fetch latest news from wire services'

    FEEDS = [
        ('Reuters', 'https://news.google.com/rss/search?q=site:reuters.com&hl=en-US&gl=US&ceid=US:en'),
        ('AP', 'https://news.google.com/rss/search?q=site:apnews.com&hl=en-US&gl=US&ceid=US:en'),
        ('BBC', 'https://feeds.bbci.co.uk/news/rss.xml'),
        ('CBS News', 'https://news.google.com/rss/search?q=site:cbsnews.com&hl=en-US&gl=US&ceid=US:en'),
        ('ABC News', 'https://news.google.com/rss/search?q=site:abcnews.com&hl=en-US&gl=US&ceid=US:en'),
        ('NBC News', 'https://news.google.com/rss/search?q=site:nbcnews.com&hl=en-US&gl=US&ceid=US:en'),
        ('Sky News', 'https://news.google.com/rss/search?q=site:news.sky.com&hl=en-US&gl=US&ceid=US:en'),
        ('CNN', 'https://news.google.com/rss/search?q=site:cnn.com&hl=en-US&gl=US&ceid=US:en'),
        ('Bloomberg', 'https://news.google.com/rss/search?q=site:bloomberg.com&hl=en-US&gl=US&ceid=US:en'),
        ('Forbes', 'https://news.google.com/rss/search?q=site:forbes.com&hl=en-US&gl=US&ceid=US:en'),
        ('Yahoo News', 'https://news.google.com/rss/search?q=site:news.yahoo.com&hl=en-US&gl=US&ceid=US:en'),
        ('Newsweek', 'https://news.google.com/rss/search?q=site:newsweek.com&hl=en-US&gl=US&ceid=US:en'),
        ('Time', 'https://news.google.com/rss/search?q=site:time.com&hl=en-US&gl=US&ceid=US:en'),
        ('Free Press', 'https://www.thefp.com/feed'),
        ('NPR', 'https://feeds.npr.org/1001/rss.xml'),
        ('France 24', 'https://www.france24.com/en/rss'),
        ('Deutsche Welle', 'https://rss.dw.com/xml/rss-en-all'),
        ('Al Jazeera', 'https://www.aljazeera.com/xml/rss/all.xml'),
        ('New York Post', 'https://nypost.com/feed/'),
        ('Washington Examiner', 'https://www.washingtonexaminer.com/feed'),
        ('Daily Caller', 'https://dailycaller.com/feed/'),
        ('The Federalist', 'https://thefederalist.com/feed/'),
        ('National Review', 'https://www.nationalreview.com/feed/'),
        ('Daily Wire', 'https://news.google.com/rss/search?q=site:dailywire.com&hl=en-US&gl=US&ceid=US:en'),
        ('Epoch Times', 'https://news.google.com/rss/search?q=site:theepochtimes.com&hl=en-US&gl=US&ceid=US:en'),
        ('Townhall', 'https://townhall.com/feed'),
        ('RedState', 'https://redstate.com/feed/'),
        ('Mother Jones', 'https://www.motherjones.com/feed/'),
        ('HuffPost', 'https://news.google.com/rss/search?q=site:huffpost.com&hl=en-US&gl=US&ceid=US:en'),
        ('The Nation', 'https://news.google.com/rss/search?q=site:thenation.com&hl=en-US&gl=US&ceid=US:en'),
        ('Salon', 'https://www.salon.com/feed'),
        ('Jacobin', 'https://jacobin.com/feed'),
        ('The Intercept', 'https://theintercept.com/feed/'),
        ('Democracy Now', 'https://news.google.com/rss/search?q=site:democracynow.org&hl=en-US&gl=US&ceid=US:en'),
        ('Common Dreams', 'https://www.commondreams.org/rss.xml'),
        ('Truthout', 'https://truthout.org/rss.xml'),
        ('Vox', 'https://news.google.com/rss/search?q=site:vox.com&hl=en-US&gl=US&ceid=US:en'),
    ]

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

    def handle(self, *args, **options):
        logger.info('Starting news fetch')
        
        cutoff = timezone.now() - timedelta(hours=24)
        
        deleted = Story.objects.filter(published__lt=cutoff).delete()
        logger.info(f'Cleaned old stories: {deleted[0]} removed')
        self.stdout.write(f"Cleaned old stories: {deleted[0]} removed")
        
        seen_urls = set(Story.objects.values_list('url', flat=True))
        total_new = 0
        total_dupes = 0
        meta_fetched = 0
        
        for source_name, feed_url in self.FEEDS:
            self.stdout.write(f"Fetching from {source_name}...", ending=" ")
            logger.info(f'Fetching from {source_name}')
            
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
        
        logger.info(f'Fetch complete: {total_new} new, {total_dupes} dupes, {meta_fetched} meta')
        self.stdout.write(self.style.SUCCESS(f"\nFetch complete: {total_new} new stories ({total_dupes} duplicates skipped, {meta_fetched} with meta descriptions)"))
