from news.languages import SUPPORTED_LANGUAGES


class ContentSecurityPolicyMiddleware:
    """Add a Content-Security-Policy response header.

    `script-src` includes 'unsafe-inline' because the AdSense/gtag snippets and
    a few legacy templates still rely on inline scripts; the ongoing JS/template
    refactor removes those, after which this can be tightened.
    """

    POLICY = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' "
        "https://www.googletagmanager.com https://www.google-analytics.com "
        "https://pagead2.googlesyndication.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self' https://www.googletagmanager.com https://www.google-analytics.com; "
        "frame-src https://pagead2.googlesyndication.com; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'self'; "
        "upgrade-insecure-requests"
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Content-Security-Policy'] = self.POLICY
        return response


class DetectLanguageMiddleware:
    """Detect preferred language from Accept-Language header.
    Sets request.detected_language which views can use as default."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        header = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        request.detected_language = self._parse(header)
        return self.get_response(request)

    def _parse(self, header):
        if not header:
            return 'en'

        langs = []
        for part in header.split(','):
            part = part.strip()
            if ';q=' in part:
                lang, q = part.split(';q=', 1)
                try:
                    quality = float(q)
                except ValueError:
                    quality = 0.1
            else:
                lang = part
                quality = 1.0

            # Extract base language (es-MX -> es, zh-CN -> zh)
            base = lang.strip().split('-')[0].lower()
            langs.append((quality, base))

        langs.sort(reverse=True)

        for _, lang in langs:
            if lang in SUPPORTED_LANGUAGES:
                return lang

        return 'en'
