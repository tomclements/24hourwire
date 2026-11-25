import os
import runpy
from unittest import mock

from django.conf import settings
from django.test import TestCase, RequestFactory, override_settings
from django.http import HttpResponse

from core.healthz import HealthzMiddleware
from news.middleware import _write_analytics_event
from news.models import AnalyticsEvent


class HealthzMiddlewareTests(TestCase):
    """Tests for the early-return /healthz middleware."""

    def test_healthz_middleware_is_first(self):
        """HealthzMiddleware must be the first entry in MIDDLEWARE."""
        from django.conf import settings
        self.assertEqual(settings.MIDDLEWARE[0], "core.healthz.HealthzMiddleware")

    def test_healthz_returns_200_ok_no_store(self):
        """GET /healthz returns 200, text/plain, and Cache-Control: no-store."""
        for path in ("/healthz", "/healthz/"):
            with self.subTest(path=path):
                with self.assertNumQueries(0):
                    response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.content.decode(), "ok")
                self.assertEqual(response["Content-Type"], "text/plain")
                self.assertEqual(response["Cache-Control"], "no-store")

    def test_healthz_no_ssl_redirect(self):
        """/healthz must not redirect even when SECURE_SSL_REDIRECT is True."""
        with override_settings(SECURE_SSL_REDIRECT=True):
            response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "ok")

    def test_healthz_does_not_set_cookies(self):
        """/healthz must not set any cookies (session, CSRF, language)."""
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.cookies, {})

    def test_healthz_middleware_short_circuits(self):
        """The middleware returns directly without calling get_response."""
        factory = RequestFactory()
        request = factory.get("/healthz")
        called = []

        def get_response(_request):
            called.append("get_response")
            return HttpResponse("should not run")

        middleware = HealthzMiddleware(get_response)
        response = middleware(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "ok")
        self.assertEqual(called, [])


class HealthzViewTests(TestCase):
    """Tests for the fallback news.views.healthz view."""

    def test_healthz_view_returns_ok_without_db(self):
        """The view returns 200 plain-text with no database access."""
        from news.views import healthz

        factory = RequestFactory()
        request = factory.get("/healthz")
        with self.assertNumQueries(0):
            response = healthz(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "ok")
        self.assertEqual(response["Content-Type"], "text/plain")


class AnalyticsConnectionLeakTests(TestCase):
    """Tests for _write_analytics_event connection handling."""

    def test_close_connections_true_closes_and_inserts(self):
        """close_connections=True inserts the row and closes the connection."""
        payload = {
            "event_type": "page_view",
            "path": "/test-leak/",
            "language": "en",
            "country_code": "US",
            "user_agent": "test-agent",
            "is_bot": False,
        }
        before = AnalyticsEvent.objects.count()

        with mock.patch("news.middleware.connection.close") as mock_close:
            _write_analytics_event(payload, close_connections=True)

        self.assertEqual(AnalyticsEvent.objects.count(), before + 1)
        event = AnalyticsEvent.objects.latest("id")
        self.assertEqual(event.path, "/test-leak/")
        # close_old_connections() calls close on stale connections, then we
        # call connection.close() explicitly in the finally block.
        self.assertGreaterEqual(mock_close.call_count, 1)

    def test_close_connections_false_does_not_close(self):
        """close_connections=False inserts the row but does not close the connection."""
        payload = {
            "event_type": "page_view",
            "path": "/test-no-leak/",
            "language": "en",
            "country_code": "US",
            "user_agent": "test-agent",
            "is_bot": False,
        }
        before = AnalyticsEvent.objects.count()

        with mock.patch("news.middleware.connection.close") as mock_close:
            _write_analytics_event(payload, close_connections=False)

        self.assertEqual(AnalyticsEvent.objects.count(), before + 1)
        mock_close.assert_not_called()


class DatabaseSettingsTests(TestCase):
    """Tests for database connection settings."""

    def test_conn_max_age_helper(self):
        """_conn_max_age reads DB_CONN_MAX_AGE and falls back to 60."""
        from core import settings as core_settings

        with mock.patch.dict(os.environ, {"DB_CONN_MAX_AGE": "120"}, clear=False):
            self.assertEqual(core_settings._conn_max_age(), 120)

        with mock.patch.dict(os.environ, {}, clear=False):
            # Ensure DB_CONN_MAX_AGE is absent.
            os.environ.pop("DB_CONN_MAX_AGE", None)
            self.assertEqual(core_settings._conn_max_age(), 60)

    def test_database_url_branch_settings(self):
        """DATABASE_URL branch sets CONN_MAX_AGE from env and CONN_HEALTH_CHECKS True."""
        import subprocess
        import sys

        env = os.environ.copy()
        env["DATABASE_URL"] = "postgresql://user:pass@localhost:5432/dbname"
        env["DB_CONN_MAX_AGE"] = "90"
        env["DEBUG"] = "True"
        env["SECRET_KEY"] = "test"

        code = (
            "from core import settings; "
            "db = settings.DATABASES['default']; "
            "print(db['CONN_MAX_AGE'], db.get('CONN_HEALTH_CHECKS'), db['OPTIONS'].get('sslmode'))"
        )
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=str(settings.BASE_DIR),
            env=env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        stdout = result.stdout.strip()
        self.assertEqual(stdout, "90 True require")


class GunicornConfigTests(TestCase):
    """Tests for gunicorn.conf.py, render.yaml and Procfile."""

    def test_gunicorn_conf_defaults(self):
        """gunicorn.conf.py loads with the expected default values."""
        with mock.patch.dict(os.environ, {}, clear=False):
            for key in ("WEB_CONCURRENCY", "GUNICORN_THREADS"):
                os.environ.pop(key, None)
            config = runpy.run_path(str(settings.BASE_DIR / "gunicorn.conf.py"))

        self.assertEqual(config["worker_class"], "gthread")
        self.assertEqual(config["workers"], 2)
        self.assertEqual(config["threads"], 8)
        self.assertEqual(config["max_requests"], 1000)
        self.assertEqual(config["max_requests_jitter"], 100)
        self.assertEqual(config["timeout"], 120)
        self.assertEqual(config["graceful_timeout"], 30)
        self.assertEqual(config["keepalive"], 5)

    def test_render_yaml_web_references_gunicorn_conf(self):
        """render.yaml web startCommand must use gunicorn.conf.py."""
        import re

        with open(settings.BASE_DIR / "render.yaml", "r", encoding="utf-8") as f:
            content = f.read()

        # Locate the web service block and its startCommand line.
        web_match = re.search(
            r"- type:\s*web\b.*?startCommand:\s*(?P<cmd>[^\n]+)",
            content,
            re.DOTALL,
        )
        self.assertIsNotNone(web_match, "No web service startCommand found")
        self.assertIn("gunicorn.conf.py", web_match.group("cmd"))

    def test_procfile_matches(self):
        """Procfile must reference gunicorn.conf.py."""
        with open(settings.BASE_DIR / "Procfile", "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("gunicorn.conf.py", content)
