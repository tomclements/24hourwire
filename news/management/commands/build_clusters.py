import logging
from django.core.management.base import BaseCommand
from news.models import build_clusters
from news.sources_config import LANGUAGE_FEEDS

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Build story clusters for all languages'

    def add_arguments(self, parser):
        parser.add_argument(
            '--language',
            type=str,
            help='Build clusters for specific language only (e.g., en, es)',
        )
        parser.add_argument(
            '--max-stories',
            type=int,
            default=500,
            help='Maximum stories to process per language (default: 500)',
        )

    def handle(self, *args, **options):
        languages = [options['language']] if options['language'] else list(LANGUAGE_FEEDS.keys())
        max_stories = options['max_stories']
        
        self.stdout.write(f"Building clusters for {len(languages)} language(s)...")
        
        total_clusters = 0
        for lang in languages:
            try:
                cluster_count = build_clusters(lang, max_stories=max_stories)
                total_clusters += cluster_count
                self.stdout.write(self.style.SUCCESS(f"Built {cluster_count} clusters for {lang}"))
            except Exception as e:
                logger.error(f'Error building clusters for {lang}: {e}')
                self.stdout.write(self.style.ERROR(f"Failed for {lang}: {e}"))
        
        self.stdout.write(self.style.SUCCESS(
            f"\nTotal clusters built: {total_clusters}"
        ))
