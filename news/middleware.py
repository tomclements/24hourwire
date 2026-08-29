"""Analytics middleware for tracking page views without collecting personal data.

Captures:
- Event type (page_view, share, feed_access, widget_load)
- URL path
- Language from query param or detected language
- Country code from Cloudflare or proxy headers
- User agent (truncated)

No IP addresses, cookies, or session data stored.
"""

import threading

from django.db import close_old_connections

from .models import AnalyticsEvent


def _write_analytics_event(payload, close_connections=False):
    """INSERT analytics row. close_connections=True when running in a worker thread."""
    if close_connections:
        close_old_connections()
    try:
        AnalyticsEvent.objects.create(**payload)
    except Exception:
        pass
    finally:
        if close_connections:
            close_old_connections()


def _schedule_analytics_write(payload):
    """Off-request-path INSERT on Postgres/gunicorn; same-connection in tests.

    Django TestCase wraps each test in a transaction. A daemon thread using a
    second SQLite connection causes "database table is locked". Production
    (PostgreSQL, ATOMIC_REQUESTS off) is not in an atomic block, so the write
    runs on a daemon thread and does not block the client.
    """
    from django.db import transaction
    if transaction.get_connection().in_atomic_block:
        _write_analytics_event(payload)
        return
    threading.Thread(
        target=_write_analytics_event,
        args=(payload, True),
        daemon=True,
    ).start()


class AnalyticsMiddleware:
    """Lightweight analytics tracking middleware."""
    
    # Paths to skip tracking
    SKIP_PATHS = [
        '/static/',
        '/media/',
        '/admin/',
        '/favicon',
        '/robots.txt',
        '/sitemap',
        '/healthz',
    ]
    
    # Bot user agent patterns (lowercase)
    # NOTE: Be careful with short patterns - 'moz' would match 'Mozilla' in every browser
    BOT_PATTERNS = [
        'bot', 'crawler', 'spider', 'slurp', 'scraper',
        'feed', 'rss', 'aggregator',
        'facebookexternalhit', 'twitterbot', 'linkedinbot',
        'whatsapp', 'telegrambot', 'slackbot',
        'googlebot', 'bingbot', 'yandex', 'baidu',
        'ahrefs', 'semrush', 'rogerbot',
        'python-requests', 'curl', 'wget', 'httpie',
        'scan', 'audit', 'check',
        'headless',  # HeadlessChrome (Playwright, Puppeteer, etc.)
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Skip tracking for certain paths
        path = request.path
        if any(path.startswith(skip) for skip in self.SKIP_PATHS):
            return response
        
        # Skip non-success responses
        if response.status_code != 200:
            return response
        
        # Determine event type from path
        event_type = self._get_event_type(path)
        
        # Get language
        language = request.GET.get('lang', getattr(request, 'detected_language', 'en'))
        
        # Get country code from headers
        country_code = self._get_country_code(request)
        
        # Get user agent (truncated)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:200]
        
        # Skip INSERT for obvious bots/crawlers (do not store a row at all)
        if self._is_bot(user_agent):
            return response

        payload = {
            "event_type": event_type,
            "path": path[:500],
            "language": language[:5] if language else "",
            "country_code": country_code[:5] if country_code else "",
            "user_agent": user_agent,
            "is_bot": False,
        }
        _schedule_analytics_write(payload)

        return response
    
    def _is_bot(self, user_agent):
        """Detect if user agent is a bot/crawler."""
        ua_lower = user_agent.lower()
        return any(pattern in ua_lower for pattern in self.BOT_PATTERNS)
    
    def _get_event_type(self, path):
        """Determine event type from URL path."""
        if path.startswith('/feed'):
            return 'feed_access'
        if path.startswith('/widget.js'):
            return 'widget_load'
        if path.startswith('/go/'):
            return 'share'
        return 'page_view'
    
    def _get_country_code(self, request):
        """Extract country code from request headers.
        
        Checks multiple headers in order of preference:
        1. Cloudflare: CF-IPCountry
        2. AWS CloudFront: CloudFront-Viewer-Country
        3. Vercel: x-vercel-ip-country
        4. Generic: X-Forwarded-For (not reliable for country)
        """
        # Cloudflare
        country = request.META.get('HTTP_CF_IPCOUNTRY')
        if country and country != 'XX':
            return country
        
        # AWS CloudFront
        country = request.META.get('HTTP_CLOUDFRONT_VIEWER_COUNTRY')
        if country:
            return country
        
        # Vercel / other proxies
        country = request.META.get('HTTP_X_VERCEL_IP_COUNTRY')
        if country:
            return country
        
        return ''
