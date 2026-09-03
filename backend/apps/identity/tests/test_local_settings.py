from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase

from config.settings import loopback_frontend_origins


class LocalFrontendOriginSettingsTests(SimpleTestCase):
    def test_builds_loopback_origins_for_configured_frontend_port(self):
        self.assertEqual(
            loopback_frontend_origins("3011"),
            ["http://localhost:3011", "http://127.0.0.1:3011"],
        )

    def test_rejects_invalid_frontend_ports(self):
        for value in ("not-a-port", "0", "65536"):
            with self.subTest(value=value), self.assertRaises(ImproperlyConfigured):
                loopback_frontend_origins(value)
