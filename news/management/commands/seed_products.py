"""Seed curated product recommendations for Amazon affiliate program.

Usage:
    python manage.py seed_products
"""

from django.core.management.base import BaseCommand
from news.models import RecommendedProduct


class Command(BaseCommand):
    help = 'Seed curated product recommendations for Amazon affiliate links'

    def handle(self, *args, **options):
        # Import inside handle so tests can patch the seasonal list.
        from news.data.amazon_products import PRODUCTS, SEASON

        names = {product_data['name'] for product_data in PRODUCTS}
        created_count = 0
        updated_count = 0

        for product_data in PRODUCTS:
            name = product_data['name']
            defaults = {
                'search_query': product_data['search_query'],
                'description': product_data['description'],
                'is_active': True,
                'language': 'en',
                'category': None,
            }

            obj, created = RecommendedProduct.objects.update_or_create(
                name=name,
                defaults=defaults,
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f'Updated: {name}'))

        # Deactivate any products that are no longer in the seasonal list.
        stale = list(RecommendedProduct.objects.filter(is_active=True).exclude(name__in=names))
        deactivated_count = len(stale)
        if stale:
            RecommendedProduct.objects.filter(pk__in=[obj.pk for obj in stale]).update(is_active=False)
            for obj in stale:
                self.stdout.write(self.style.WARNING(f'Deactivated: {obj.name}'))

        self.stdout.write(self.style.SUCCESS(
            f'\nSeason: {SEASON}. {created_count} created, {updated_count} updated, '
            f'{deactivated_count} deactivated, {len(PRODUCTS)} active products.'
        ))
