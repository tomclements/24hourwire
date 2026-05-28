#!/usr/bin/env python
"""Seed initial polls for review and testing.

Usage:
    python manage.py seed_polls           # Create default polls
    python manage.py seed_polls --clear   # Delete all polls first
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from news.models import Poll


INITIAL_POLLS = [
    {
        'language': 'en',
        'question': 'Which news topic interests you most right now?',
        'options': ['World affairs', 'Technology', 'Sports', 'Business & markets', 'Science & health'],
        'poll_type': 'topical',
        'english_translation': 'Which news topic interests you most right now?',
        'ends_at_days': 14,
    },
    {
        'language': 'en',
        'question': 'How do you prefer to get your news?',
        'options': ['Social media', 'News websites', 'Email newsletters', 'Podcasts', 'TV/Radio'],
        'poll_type': 'lifestyle',
        'english_translation': 'How do you prefer to get your news?',
        'ends_at_days': 30,
    },
    {
        'language': 'en',
        'question': 'Should social media platforms be responsible for fact-checking news?',
        'options': ['Yes — platforms should verify', 'No — users should judge', 'Only for paid political ads'],
        'poll_type': 'opinion',
        'english_translation': 'Should social media platforms be responsible for fact-checking news?',
        'ends_at_days': 21,
    },
    {
        'language': 'en',
        'question': 'What\'s your go-to coffee while reading the morning headlines?',
        'options': ['Black coffee', 'Latte / Cappuccino', 'Tea', 'Cold brew', 'No caffeine'],
        'poll_type': 'fun',
        'english_translation': 'What\'s your go-to coffee while reading the morning headlines?',
        'ends_at_days': 14,
    },
    {
        'language': 'es',
        'question': '¿Qué tema de noticias te interesa más en este momento?',
        'options': ['Asuntos mundiales', 'Tecnología', 'Deportes', 'Negocios', 'Ciencia y salud'],
        'poll_type': 'topical',
        'english_translation': 'Which news topic interests you most right now?',
        'ends_at_days': 14,
    },
    {
        'language': 'fr',
        'question': 'Quelle source d\'information faites-vous le plus confiance?',
        'options': ['Médias traditionnels', 'Réseaux sociaux', 'Agrégateurs', 'Newsletters', 'Radio/TV'],
        'poll_type': 'opinion',
        'english_translation': 'Which news source do you trust the most?',
        'ends_at_days': 21,
    },
]


class Command(BaseCommand):
    help = 'Seed initial poll candidates for staff review'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing polls before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            count = Poll.objects.all().count()
            Poll.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {count} existing polls.'))

        created_count = 0
        skipped_count = 0

        for data in INITIAL_POLLS:
            # Skip if identical question exists in last 30 days
            if Poll.objects.filter(
                language=data['language'],
                question__iexact=data['question'],
                created_at__gte=timezone.now() - timedelta(days=30),
            ).exists():
                self.stdout.write(self.style.WARNING(
                    f"Skipped (already exists): {data['question'][:50]}..."
                ))
                skipped_count += 1
                continue

            poll = Poll.objects.create(
                language=data['language'],
                question=data['question'],
                options=data['options'],
                poll_type=data['poll_type'],
                english_translation=data['english_translation'],
                status='pending_review',
                is_active=False,
                ends_at=timezone.now() + timedelta(days=data['ends_at_days']),
                source='manual',
            )
            created_count += 1
            self.stdout.write(self.style.SUCCESS(
                f"Created [{poll.language}]: {poll.question[:60]}..."
            ))

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! Created {created_count} polls, skipped {skipped_count} duplicates."
        ))
        self.stdout.write(
            f"\nNext step: Visit /polls/manage/ to review and activate polls."
        )
