"""Seed curated book recommendations for Amazon affiliate program.

Usage:
    python manage.py seed_books
    python manage.py seed_books --update  # Refresh existing
"""

from django.core.management.base import BaseCommand
from news.models import RecommendedBook


BOOKS = [
    # WORLD
    {
        'title': 'The World: A Brief Introduction',
        'author': 'Richard Haass',
        'asin': 'B082WP8PKP',
        'category': 'world',
        'description': 'A primer on global politics, economics, and the forces shaping our interconnected world.',
    },
    {
        'title': 'Prisoners of Geography',
        'author': 'Tim Marshall',
        'asin': '1501121472',
        'category': 'world',
        'description': 'How maps and terrain explain the conflicts and alliances of nations.',
    },
    {
        'title': 'The Chaos Machine',
        'author': 'Max Fisher',
        'asin': '0063159882',
        'category': 'world',
        'description': 'How social media algorithms amplify outrage and reshape global society.',
    },
    # POLITICS
    {
        'title': 'The Righteous Mind',
        'author': 'Jonathan Haidt',
        'asin': '0307455777',
        'category': 'politics',
        'description': 'Why good people disagree about politics and religion — essential for understanding both sides.',
    },
    {
        'title': 'Why We\'re Polarized',
        'author': 'Ezra Klein',
        'asin': '147670032X',
        'category': 'politics',
        'description': 'An exploration of how identity and media have divided American politics.',
    },
    {
        'title': 'How Democracies Die',
        'author': 'Steven Levitsky & Daniel Ziblatt',
        'asin': '1524762938',
        'category': 'politics',
        'description': 'The warning signs of democratic backsliding and how to prevent it.',
    },
    # BUSINESS
    {
        'title': 'The Everything Store',
        'author': 'Brad Stone',
        'asin': '0316219282',
        'category': 'business',
        'description': 'The inside story of Amazon and how it reshaped commerce and work.',
    },
    {
        'title': 'Flash Boys',
        'author': 'Michael Lewis',
        'asin': '0393244660',
        'category': 'business',
        'description': 'How high-frequency trading rigs the market against ordinary investors.',
    },
    {
        'title': 'The Divide',
        'author': 'Matt Taibbi',
        'asin': '081299342X',
        'category': 'business',
        'description': 'The growing gap between the wealthy and everyone else in America.',
    },
    # TECHNOLOGY
    {
        'title': 'The Social Dilemma Companion Book',
        'author': 'Jeff Orlowski',
        'asin': 'B08JQLH7M7',
        'category': 'technology',
        'description': 'How social media platforms manipulate behavior and reshape society.',
    },
    {
        'title': 'Tools and Weapons',
        'author': 'Brad Smith & Carol Ann Browne',
        'asin': '1984877712',
        'category': 'technology',
        'description': 'The promise and peril of the digital age from Microsoft\'s president.',
    },
    {
        'title': 'The Age of Surveillance Capitalism',
        'author': 'Shoshana Zuboff',
        'asin': '1610395697',
        'category': 'technology',
        'description': 'How tech companies harvest human experience as raw material for profit.',
    },
    # SCIENCE
    {
        'title': 'The Body: A Guide for Occupants',
        'author': 'Bill Bryson',
        'asin': '0385539304',
        'category': 'science',
        'description': 'An accessible journey through the human body and the science that keeps it running.',
    },
    {
        'title': 'Merchants of Doubt',
        'author': 'Naomi Oreskes & Erik Conway',
        'asin': '1608193942',
        'category': 'science',
        'description': 'How a handful of scientists obscured the truth on issues from tobacco to climate change.',
    },
    {
        'title': 'Sapiens',
        'author': 'Yuval Noah Harari',
        'asin': '0062316095',
        'category': 'science',
        'description': 'A brief history of humankind that puts current events in evolutionary context.',
    },
]


class Command(BaseCommand):
    help = 'Seed curated book recommendations for Amazon affiliate links'

    def add_arguments(self, parser):
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing books instead of skipping',
        )

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0
        
        for book_data in BOOKS:
            asin = book_data['asin']
            
            if RecommendedBook.objects.filter(asin=asin).exists():
                if options['update']:
                    RecommendedBook.objects.filter(asin=asin).update(**book_data)
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Updated: {book_data["title"]}'))
                else:
                    self.stdout.write(f'Skipped (exists): {book_data["title"]}')
                continue
            
            RecommendedBook.objects.create(**book_data)
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'Created: {book_data["title"]}'))
        
        self.stdout.write(self.style.SUCCESS(
            f'\nDone! {created_count} created, {updated_count} updated, '
            f'{len(BOOKS) - created_count - updated_count} skipped.'
        ))
