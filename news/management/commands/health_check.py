import feedparser
import urllib.request
import ssl
import logging
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from news.sources_config import LANGUAGE_FEEDS

logger = logging.getLogger('news.health')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('health_check.log', encoding='utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


class Command(BaseCommand):
    help = 'Check health of all RSS feeds and email summary'

    def safe_write(self, msg, **kwargs):
        try:
            self.stdout.write(msg, **kwargs)
        except UnicodeEncodeError:
            self.stdout.write(msg.encode('ascii', 'replace').decode('ascii'), **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('--email', action='store_true', help='Send email summary')
        parser.add_argument('--to', type=str, default='', help='Email recipient')

    def test_feed(self, name, url, language):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
                feed = feedparser.parse(response.read())
                if feed.entries:
                    return 'ok', len(feed.entries)
                else:
                    return 'empty', 0
        except Exception as e:
            error_msg = str(e)[:80]
            return f'error: {error_msg}', 0

    def handle(self, *args, **options):
        self.safe_write("Running feed health check...\n")

        results = {}  # language -> list of (name, status, count)
        total_feeds = 0
        total_ok = 0
        total_empty = 0
        total_error = 0

        for language, feeds in sorted(LANGUAGE_FEEDS.items()):
            results[language] = []
            for source_name, feed_url in feeds:
                total_feeds += 1
                status, count = self.test_feed(source_name, feed_url, language)
                results[language].append((source_name, status, count))

                if status == 'ok':
                    total_ok += 1
                elif status == 'empty':
                    total_empty += 1
                else:
                    total_error += 1
                    logger.warning(f'{language}/{source_name}: {status}')

        # Build report
        lines = []
        lines.append(f"24HourWire Feed Health Check — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"{'=' * 60}")
        lines.append(f"Total feeds: {total_feeds}  OK: {total_ok}  Empty: {total_empty}  Errors: {total_error}")
        lines.append("")

        for language in sorted(results.keys()):
            lang_feeds = results[language]
            errors = [(n, s, c) for n, s, c in lang_feeds if s != 'ok']
            empties = [(n, s, c) for n, s, c in lang_feeds if s == 'empty']
            oks = [(n, s, c) for n, s, c in lang_feeds if s == 'ok']

            lines.append(f"[{language.upper()}] {len(oks)} ok, {len(empties)} empty, {len(errors)} errors")

            if errors:
                for name, status, _ in errors:
                    lines.append(f"  FAIL: {name} — {status}")
            if empties:
                for name, _, _ in empties:
                    lines.append(f"  EMPTY: {name}")

        lines.append("")
        lines.append("Action items:")
        broken = [(lang, n, s) for lang in results for n, s, c in results[lang] if s != 'ok' and s != 'empty']
        if broken:
            lines.append(f"  - {len(broken)} feeds returning errors — check if URLs are still valid")
        stale = [(lang, n) for lang in results for n, s, c in results[lang] if s == 'empty']
        if stale:
            lines.append(f"  - {len(stale)} feeds returning 0 entries — may be dead or changed format")
        if not broken and not stale:
            lines.append("  - All feeds healthy!")

        report = "\n".join(lines)
        self.safe_write(report)

        # Email if requested
        if options['email']:
            to_email = options['to'] or getattr(settings, 'HEALTH_CHECK_EMAIL', '')
            if not to_email:
                self.safe_write(self.style.WARNING("No recipient email specified. Use --to or set HEALTH_CHECK_EMAIL in settings."))
                return

            smtp_host = getattr(settings, 'EMAIL_HOST', '')
            smtp_port = getattr(settings, 'EMAIL_PORT', 587)
            smtp_user = getattr(settings, 'EMAIL_HOST_USER', '')
            smtp_pass = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
            from_email = getattr(settings, 'EMAIL_FROM', smtp_user)

            if not smtp_host:
                self.safe_write(self.style.WARNING("EMAIL_HOST not configured in settings."))
                return

            try:
                msg = MIMEText(report)
                msg['Subject'] = f'24HourWire Health Check — {total_error} errors, {total_empty} empty'
                msg['From'] = from_email
                msg['To'] = to_email

                with smtplib.SMTP(smtp_host, smtp_port) as server:
                    server.starttls()
                    if smtp_user:
                        server.login(smtp_user, smtp_pass)
                    server.sendmail(from_email, [to_email], msg.as_string())

                self.safe_write(self.style.SUCCESS(f"\nEmail sent to {to_email}"))
            except Exception as e:
                self.safe_write(self.style.ERROR(f"\nFailed to send email: {e}"))
