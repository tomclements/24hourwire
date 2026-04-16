"""
Management command to check fetch status and diagnose stale stories issue.
Run: python manage.py check_fetch_status
"""

from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from news.models import Story


class Command(BaseCommand):
    help = 'Check fetch status and diagnose stale stories'

    def handle(self, *args, **options):
        now = timezone.now()
        
        # Get story counts by time ranges
        total_stories = Story.objects.count()
        
        recent_1h = Story.objects.filter(published__gte=now - timedelta(hours=1)).count()
        recent_3h = Story.objects.filter(published__gte=now - timedelta(hours=3)).count()
        recent_6h = Story.objects.filter(published__gte=now - timedelta(hours=6)).count()
        recent_12h = Story.objects.filter(published__gte=now - timedelta(hours=12)).count()
        recent_24h = Story.objects.filter(published__gte=now - timedelta(hours=24)).count()
        
        oldest_story = Story.objects.order_by('published').first()
        newest_story = Story.objects.order_by('-published').first()
        
        self.stdout.write("=" * 60)
        self.stdout.write("FETCH STATUS DIAGNOSTIC")
        self.stdout.write("=" * 60)
        self.stdout.write(f"Current time: {now}")
        self.stdout.write(f"Total stories in database: {total_stories}")
        self.stdout.write("")
        self.stdout.write("Stories by time range:")
        self.stdout.write(f"  Last 1 hour:  {recent_1h}")
        self.stdout.write(f"  Last 3 hours: {recent_3h}")
        self.stdout.write(f"  Last 6 hours: {recent_6h}")
        self.stdout.write(f"  Last 12 hours: {recent_12h}")
        self.stdout.write(f"  Last 24 hours: {recent_24h}")
        self.stdout.write("")
        
        if newest_story:
            self.stdout.write(f"Newest story: {newest_story.title[:50]}...")
            self.stdout.write(f"  Published: {newest_story.published}")
            self.stdout.write(f"  Source: {newest_story.source}")
            self.stdout.write(f"  Age: {now - newest_story.published}")
        else:
            self.stdout.write(self.style.ERROR("No stories in database!"))
        
        self.stdout.write("")
        
        if oldest_story:
            self.stdout.write(f"Oldest story: {oldest_story.title[:50]}...")
            self.stdout.write(f"  Published: {oldest_story.published}")
            self.stdout.write(f"  Source: {oldest_story.source}")
        
        self.stdout.write("")
        
        # Check by language
        self.stdout.write("Stories by language:")
        languages = Story.objects.values_list('language', flat=True).distinct()
        for lang in languages:
            count = Story.objects.filter(language=lang).count()
            recent = Story.objects.filter(language=lang, published__gte=now - timedelta(hours=6)).count()
            self.stdout.write(f"  {lang}: {count} total, {recent} in last 6h")
        
        self.stdout.write("")
        
        # Check by source
        self.stdout.write("Top 10 sources by story count:")
        sources = Story.objects.values_list('source', flat=True).distinct()[:10]
        for source in sources:
            count = Story.objects.filter(source=source).count()
            recent = Story.objects.filter(source=source, published__gte=now - timedelta(hours=6)).count()
            status = "OK" if recent > 0 else "STALE"
            style = self.style.SUCCESS if recent > 0 else self.style.ERROR
            self.stdout.write(style(f"  {source}: {count} total, {recent} in last 6h [{status}]"))
        
        self.stdout.write("")
        
        # Diagnosis
        if recent_1h == 0:
            self.stdout.write(self.style.ERROR("WARNING: No stories in last hour!"))
            self.stdout.write("Possible causes:")
            self.stdout.write("  1. fetch_news command not running (check cron job)")
            self.stdout.write("  2. All RSS feeds returning empty")
            self.stdout.write("  3. Network/connectivity issues")
            self.stdout.write("  4. Memory limits causing process to fail")
            self.stdout.write("")
            self.stdout.write("Check fetch_news.log for details")
        elif recent_1h < 5:
            self.stdout.write(self.style.WARNING("WARNING: Very few stories in last hour"))
        else:
            self.stdout.write(self.style.SUCCESS("Fetch appears to be working normally"))
