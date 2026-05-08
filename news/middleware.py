"""Analytics middleware for tracking page views without collecting personal data.

Captures:
- Event type (page_view, share, feed_access, widget_load)
- URL path
- Language from query param or detected language
- Country code from Cloudflare or proxy headers
- User agent (truncated)

No IP addresses, cookies, or session data stored.
"""

from .models import AnalyticsEvent


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
        
        # Detect if request is from a bot/crawler
        is_bot = self._is_bot(user_agent)
        
        # Log the event asynchronously to avoid slowing down response
        try:
            AnalyticsEvent.objects.create(
                event_type=event_type,
                path=path[:500],
                language=language[:5],
                country_code=country_code[:5],
                user_agent=user_agent,
                is_bot=is_bot,
            )
        except Exception:
            # Silently fail if analytics logging breaks
            pass
        
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
