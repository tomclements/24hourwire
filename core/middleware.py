from news.languages import SUPPORTED_LANGUAGES


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
