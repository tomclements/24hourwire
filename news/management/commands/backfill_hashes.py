from django.core.management.base import BaseCommand
from news.models import Story, normalize_url, title_fingerprint
import hashlib


class Command(BaseCommand):
    help = 'Backfill url_hash and title_fingerprint on existing stories'

    def handle(self, *args, **options):
        stories = Story.objects.filter(url_hash='')
        total = stories.count()
        self.stdout.write(f"Found {total} stories to backfill")

        updated = 0
        for story in stories.iterator():
            story.url_hash = hashlib.sha256(normalize_url(story.url).encode()).hexdigest()
            story.title_fingerprint = title_fingerprint(story.title)
            story.save(update_fields=['url_hash', 'title_fingerprint'])
            updated += 1
            if updated % 500 == 0:
                self.stdout.write(f"  {updated}/{total}")

        self.stdout.write(self.style.SUCCESS(f"Backfilled {updated} stories"))
