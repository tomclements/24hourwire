"""Seed a few recent English stories so Playwright CI has .story-card rows.

Usage:
    python manage.py seed_playwright_stories
"""

import hashlib

from django.core.management.base import BaseCommand
from django.utils import timezone

from news.models import Story, StoryCategory, normalize_url, title_fingerprint


SEED_STORIES = [
    {
        'source': 'Reuters',
        'title': 'Playwright seed: global markets open higher after trade talks',
        'excerpt': 'A fixture English story used only to populate the homepage for Playwright tests.',
        'url': 'https://example.com/playwright-seed/1',
        'category': 'world',
        'slugs': ['world'],
    },
    {
        'source': 'BBC',
        'title': 'Playwright seed: new chip design speeds up data centers',
        'excerpt': 'A second fixture English story so Different Angle tests can use two cards.',
        'url': 'https://example.com/playwright-seed/2',
        'category': 'technology',
        'slugs': ['technology'],
    },
    {
        'source': 'AP',
        'title': 'Playwright seed: lawmakers debate budget ahead of deadline',
        'excerpt': 'A third fixture English story so category tabs have more than one group.',
        'url': 'https://example.com/playwright-seed/3',
        'category': 'politics',
        'slugs': ['politics'],
    },
]


class Command(BaseCommand):
    help = 'Seed recent English stories for Playwright homepage tests'

    def handle(self, *args, **options):
        now = timezone.now()
        created = 0
        updated = 0

        for data in SEED_STORIES:
            slugs = data['slugs']
            url = data['url']
            url_hash = hashlib.sha256(normalize_url(url).encode()).hexdigest()
            fp = title_fingerprint(data['title'])
            defaults = {
                'source': data['source'],
                'title': data['title'],
                'excerpt': data['excerpt'],
                'language': 'en',
                'category': data['category'],
                'published': now,
                'url_hash': url_hash,
                'title_fingerprint': fp,
            }
            story, was_created = Story.objects.update_or_create(
                url=url,
                defaults=defaults,
            )
            if was_created:
                created += 1
            else:
                updated += 1
            for slug in slugs:
                StoryCategory.objects.get_or_create(story=story, slug=slug)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded Playwright stories: created={created} updated={updated}'
        ))
