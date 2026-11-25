from django.http import HttpResponse


class HealthzMiddleware:
    """Answer Render's /healthz probe immediately, before any other middleware.

    Runs as the first middleware so it bypasses HTTPS redirect, sessions, CSRF,
    and any heavy work that would make the probe queue behind slow requests.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in ("/healthz", "/healthz/"):
            response = HttpResponse("ok", content_type="text/plain")
            response["Cache-Control"] = "no-store"
            return response
        return self.get_response(request)
