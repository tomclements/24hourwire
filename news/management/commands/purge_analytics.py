from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from news.models import AnalyticsEvent


class Command(BaseCommand):
    help = (
        "Delete AnalyticsEvent rows older than the retention window so the table "
        "does not grow forever on basic-256mb Postgres. Default retention is 7 days "
        "(analytics dashboards use 7-day windows). Stories themselves expire at 24h; "
        "analytics keeps a longer window on purpose. Override with --days."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=7,
            help="Retention in days (default: 7). Rows older than this are deleted.",
        )

    def handle(self, *args, **options):
        days = options["days"]
        if days < 1:
            self.stderr.write(self.style.ERROR("--days must be >= 1"))
            return
        cutoff = timezone.now() - timedelta(days=days)
        deleted, _ = AnalyticsEvent.objects.filter(timestamp__lt=cutoff).delete()
        self.stdout.write(self.style.SUCCESS(
            f"Purged {deleted} analytics event(s) older than {days} day(s)."
        ))
