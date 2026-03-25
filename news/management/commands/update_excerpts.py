import urllib.request
import ssl
import re
import logging
from django.core.management.base import BaseCommand
from news.models import Story

logger = logging.getLogger('news.update')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('fetch_news.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


class Command(BaseCommand):
    help = 'Fetch meta descriptions for existing stories'

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
                
                match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', html, re.I)
                if not match:
                    match = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']', html, re.I)
                
                if match:
                    desc = match.group(1).strip()
                    desc = desc.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
                    return desc[:500]
                
                match = re.search(r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']+)["\']', html, re.I)
                if match:
                    return match.group(1).strip()[:500]
                    
        except Exception:
            pass
        return ''

    def handle(self, *args, **options):
        logger.info('Starting excerpt update')
        
        stories = Story.objects.filter(excerpt__isnull=True) | Story.objects.extra(where=["LENGTH(excerpt) < 30"])
        stories = list(stories[:100])
        
        updated = 0
        for story in stories:
            meta = self.get_meta_description(story.url)
            if meta:
                story.excerpt = meta
                story.save()
                updated += 1
                logger.info(f'{story.source}: {meta[:50]}...')
                self.stdout.write(f"  {story.source}: {meta[:50]}...")
        
        logger.info(f'Updated {updated} stories')
        self.stdout.write(self.style.SUCCESS(f"\nUpdated {updated} stories with meta descriptions"))
