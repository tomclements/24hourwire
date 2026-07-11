import json
import os
import feedparser
import urllib.request
import ssl
import concurrent.futures
import logging
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from news.sources_config import LANGUAGE_FEEDS

logger = logging.getLogger('news.monitor')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('feed_monitor.log', encoding='utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

STATUS_FILE = 'feed_status.json'


def load_status():
    """Load feed status tracking from JSON file."""
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {
        'disabled_feeds': {},  # language -> {source_name: reason}
        'feed_history': {},    # language/source_name -> {failures: int, last_check: str, last_status: str}
        'last_run': None,
    }


def save_status(status):
    """Save feed status tracking to JSON file."""
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status, f, ensure_ascii=False, indent=2)


def test_feed(name, url, timeout=10):
    """Test a single feed and return (name, status, count, error)."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml, */*;q=0.8',
        })
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as response:
            feed = feedparser.parse(response.read())
            if feed.entries:
                return name, 'ok', len(feed.entries), None
            else:
                return name, 'empty', 0, None
    except Exception as e:
        error_msg = str(e)[:100]
        return name, 'error', 0, error_msg


def get_all_feeds(language_filter=None):
    """Return list of (language, source_name, url) tuples."""
    feeds = []
    for language, lang_feeds in sorted(LANGUAGE_FEEDS.items()):
        if language_filter and language != language_filter:
            continue
        for source_name, feed_url in lang_feeds:
            feeds.append((language, source_name, feed_url))
    return feeds


class Command(BaseCommand):
    help = 'Monitor RSS feed health, track failures, and optionally disable broken feeds'

    def add_arguments(self, parser):
        parser.add_argument('--language', type=str, default='', help='Only monitor feeds for this language')
        parser.add_argument('--timeout', type=int, default=10, help='Feed request timeout in seconds')
        parser.add_argument('--workers', type=int, default=8, help='Number of parallel workers')
        parser.add_argument('--disable-after', type=int, default=3, help='Disable feeds after N consecutive failures')
        parser.add_argument('--auto-disable', action='store_true', help='Automatically disable persistently failing feeds')
        parser.add_argument('--report-only', action='store_true', help='Only report status without disabling feeds')
        parser.add_argument('--enable-working', action='store_true', help='Re-enable previously disabled feeds that are now working')

    def safe_write(self, msg, **kwargs):
        try:
            self.stdout.write(msg, **kwargs)
        except UnicodeEncodeError:
            import sys
            self.stdout.write(msg.encode(sys.stdout.encoding or 'utf-8', 'replace').decode(sys.stdout.encoding or 'utf-8'), **kwargs)

    def handle(self, *args, **options):
        language_filter = options['language'].lower()
        timeout = options['timeout']
        workers = options['workers']
        disable_after = options['disable_after']
        auto_disable = options['auto_disable']
        report_only = options['report_only']
        enable_working = options['enable_working']

        status = load_status()
        feeds = get_all_feeds(language_filter)

        self.safe_write(f"Monitoring {len(feeds)} feeds (timeout={timeout}s, workers={workers})...\n")

        results_by_lang = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_feed = {
                executor.submit(test_feed, name, url, timeout): (language, name, url)
                for language, name, url in feeds
            }
            for future in concurrent.futures.as_completed(future_to_feed):
                language, name, url = future_to_feed[future]
                _, feed_status, count, error = future.result()

                if language not in results_by_lang:
                    results_by_lang[language] = []
                results_by_lang[language].append((name, url, feed_status, count, error))

        # Update status tracking
        now = datetime.now().isoformat()
        status['last_run'] = now

        changed_feeds = []
        newly_disabled = []
        re_enabled = []

        for language, lang_results in results_by_lang.items():
            if language not in status['feed_history']:
                status['feed_history'][language] = {}
            if language not in status['disabled_feeds']:
                status['disabled_feeds'][language] = {}

            for name, url, feed_status, count, error in lang_results:
                history = status['feed_history'][language].get(name, {
                    'failures': 0,
                    'last_check': None,
                    'last_status': None,
                })

                history['last_check'] = now
                history['last_status'] = feed_status

                if feed_status == 'ok':
                    if history['failures'] > 0:
                        changed_feeds.append((language, name, 'back to OK'))
                    history['failures'] = 0

                    # Re-enable if it was disabled and now working
                    if enable_working and name in status['disabled_feeds'].get(language, {}):
                        del status['disabled_feeds'][language][name]
                        re_enabled.append((language, name))
                else:
                    history['failures'] += 1
                    if history['failures'] >= disable_after:
                        if auto_disable and name not in status['disabled_feeds'][language]:
                            status['disabled_feeds'][language][name] = {
                                'reason': error or feed_status,
                                'disabled_at': now,
                                'url': url,
                            }
                            newly_disabled.append((language, name, error or feed_status))

                status['feed_history'][language][name] = history

        save_status(status)

        # Build report
        total_feeds = sum(len(r) for r in results_by_lang.values())
        total_ok = sum(1 for lang in results_by_lang.values() for _, _, s, _, _ in lang if s == 'ok')
        total_empty = sum(1 for lang in results_by_lang.values() for _, _, s, _, _ in lang if s == 'empty')
        total_error = sum(1 for lang in results_by_lang.values() for _, _, s, _, _ in lang if s == 'error')

        lines = []
        lines.append(f"24HourWire Feed Monitor — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"{'=' * 60}")
        lines.append(f"Total feeds checked: {total_feeds}")
        lines.append(f"OK: {total_ok} | Empty: {total_empty} | Errors: {total_error}")

        if newly_disabled:
            lines.append(f"\nNewly disabled feeds ({len(newly_disabled)}):")
            for lang, name, reason in newly_disabled:
                lines.append(f"  [{lang}] {name} — {reason}")

        if re_enabled:
            lines.append(f"\nRe-enabled feeds ({len(re_enabled)}):")
            for lang, name in re_enabled:
                lines.append(f"  [{lang}] {name}")

        # Show currently disabled feeds
        all_disabled = []
        for lang, feeds in status['disabled_feeds'].items():
            for name, info in feeds.items():
                all_disabled.append((lang, name, info.get('reason', 'unknown')))

        if all_disabled:
            lines.append(f"\nCurrently disabled feeds ({len(all_disabled)}):")
            for lang, name, reason in sorted(all_disabled):
                lines.append(f"  [{lang}] {name} — {reason}")

        # Show current errors
        current_errors = []
        for lang, lang_results in results_by_lang.items():
            for name, url, feed_status, count, error in lang_results:
                if feed_status == 'error':
                    current_errors.append((lang, name, error or 'error'))

        if current_errors:
            lines.append(f"\nCurrent errors ({len(current_errors)}):")
            for lang, name, error in sorted(current_errors):
                lines.append(f"  [{lang}] {name} — {error}")

        report = "\n".join(lines)
        self.safe_write(report)

        if auto_disable:
            logger.info(f"Monitor complete: {total_ok} ok, {total_empty} empty, {total_error} error, {len(newly_disabled)} newly disabled, {len(re_enabled)} re-enabled")
        else:
            logger.info(f"Monitor complete: {total_ok} ok, {total_empty} empty, {total_error} error (report-only mode)")

        self.safe_write(f"\nStatus saved to {STATUS_FILE}")
