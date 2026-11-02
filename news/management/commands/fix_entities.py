from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from news.models import Story, normalize_stored_title, normalize_text, title_fingerprint


class Command(BaseCommand):
    help = 'Fix double-encoded HTML entities in story titles and excerpts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--apply',
            action='store_true',
            dest='apply',
            default=False,
            help='Apply fixes to the database (default is dry-run)',
        )

    def handle(self, *args, **options):
        apply = options['apply']
        mode = 'APPLY' if apply else 'DRY-RUN'
        self.stdout.write(self.style.NOTICE(f'fix_entities: running in {mode} mode'))

        changed_by_source = {}
        examined = 0
        changed = 0
        unchanged = 0
        skipped = 0

        stories = Story.objects.only('id', 'source', 'title', 'excerpt', 'title_fingerprint').iterator()
        for story in stories:
            examined += 1
            new_title = normalize_stored_title(story.title)
            new_excerpt = normalize_text(story.excerpt)
            new_fingerprint = title_fingerprint(new_title)

            title_changed = new_title != story.title
            excerpt_changed = new_excerpt != story.excerpt
            fingerprint_changed = new_fingerprint != story.title_fingerprint

            if title_changed or excerpt_changed or fingerprint_changed:
                changed += 1
                changed_by_source[story.source] = changed_by_source.get(story.source, 0) + 1
                if apply:
                    try:
                        with transaction.atomic():
                            story.title = new_title
                            story.excerpt = new_excerpt
                            story.title_fingerprint = new_fingerprint
                            story.save(update_fields=['title', 'excerpt', 'title_fingerprint'])
                    except IntegrityError as e:
                        skipped += 1
                        self.stderr.write(f'IntegrityError fixing story {story.id}: {e}')
                        continue
            else:
                unchanged += 1

        self.stdout.write(f'Examined: {examined}')
        self.stdout.write(f'Changed:  {changed}')
        self.stdout.write(f'Unchanged: {unchanged}')
        if skipped:
            self.stdout.write(f'Skipped:  {skipped}')

        if changed_by_source:
            self.stdout.write('Changes by source:')
            for source, count in sorted(changed_by_source.items()):
                self.stdout.write(f'  {source}: {count}')

        if not apply and changed > 0:
            self.stdout.write(self.style.WARNING('Run with --apply to persist these changes.'))
        elif apply and changed > 0:
            self.stdout.write(self.style.SUCCESS(f'Updated {changed} stories.'))
        else:
            self.stdout.write(self.style.SUCCESS('No changes needed.'))
