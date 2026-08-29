from news.languages import SUPPORTED_LANGUAGES


class ContentSecurityPolicyMiddleware:
    """Add a Content-Security-Policy response header.

    First-party JS lives in static files. JSON-LD and application/json script
    tags are not executable. Google tag / AdSense hosts remain allowed.
    """

    POLICY = (
        "default-src 'self'; "
        "script-src 'self' "
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

    Sets request.detected_language (Accept-Language only) for views.
    Also sets request.LANGUAGE_CODE to the language the views will render
    (?lang= override, else detected_language) so Django cache_page keys
    differ by language. LocaleMiddleware is not used; with USE_I18N=True,
    learn_cache_key strips Accept-Language and suffixes LANGUAGE_CODE.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        header = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        request.detected_language = self._parse(header)
        language = request.GET.get('lang', request.detected_language)
        if language not in SUPPORTED_LANGUAGES:
            language = 'en'
        request.LANGUAGE_CODE = language
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
