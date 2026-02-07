"""Tests for Discord Ed25519 signature verification."""

from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase
from nacl.signing import SigningKey


class VerifyTest(SimpleTestCase):
    """Test the verify() function with real Ed25519 signatures."""

    def setUp(self):
        # Generate a fresh key-pair for each test.
        self.signing_key = SigningKey.generate()
        self.verify_hex = self.signing_key.verify_key.encode().hex()

    def _make_request(self, body=b'{"type":1}', timestamp="1234567890"):
        """Build a request and sign it with the test signing key."""
        factory = RequestFactory()
        request = factory.post(
            "/discord/interactions/",
            data=body,
            content_type="application/json",
        )

        # Compute a valid Ed25519 signature.
        message = f"{timestamp}{body.decode()}".encode()
        signed = self.signing_key.sign(message)
        sig_hex = signed.signature.hex()

        request.META["HTTP_X_SIGNATURE_ED25519"] = sig_hex
        request.META["HTTP_X_SIGNATURE_TIMESTAMP"] = timestamp
        return request

    @patch("apps.discord.interactions.verify.settings")
    def test_valid_signature_succeeds(self, mock_settings):
        """A correctly signed request should not raise."""
        mock_settings.DISCORD = {"PUBLIC_KEY": self.verify_hex}

        from apps.discord.interactions.verify import verify

        request = self._make_request()
        # Should return without raising.
        verify(request)

    @patch("apps.discord.interactions.verify.settings")
    def test_tampered_body_raises(self, mock_settings):
        """Altering the body after signing should raise BadSignatureError."""
        from nacl.exceptions import BadSignatureError

        mock_settings.DISCORD = {"PUBLIC_KEY": self.verify_hex}

        from apps.discord.interactions.verify import verify

        request = self._make_request(body=b'{"type":1}')
        # Tamper with the body after the signature was computed.
        request._body = b'{"type":2}'

        with self.assertRaises(BadSignatureError):
            verify(request)

    @patch("apps.discord.interactions.verify.settings")
    def test_missing_signature_raises_value_error(self, mock_settings):
        mock_settings.DISCORD = {"PUBLIC_KEY": self.verify_hex}

        from apps.discord.interactions.verify import verify

        factory = RequestFactory()
        request = factory.post(
            "/discord/interactions/",
            data=b'{"type":1}',
            content_type="application/json",
        )
        # No signature headers at all.
        with self.assertRaises(ValueError):
            verify(request)

    @patch("apps.discord.interactions.verify.settings")
    def test_missing_timestamp_raises_value_error(self, mock_settings):
        mock_settings.DISCORD = {"PUBLIC_KEY": self.verify_hex}

        from apps.discord.interactions.verify import verify

        request = self._make_request()
        # Remove the timestamp header.
        del request.META["HTTP_X_SIGNATURE_TIMESTAMP"]

        with self.assertRaises(ValueError):
            verify(request)


class VerifySlashRouterTest(SimpleTestCase):
    """Smoke-test that the slash router correctly dispatches."""

    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/leaders/")
    def test_slash_dispatches_known_command(self, _rev):
        """The router should find 'leaders' in the registry."""
        from apps.discord.interactions.handlers.slash import slash

        factory = RequestFactory()
        request = factory.post("/discord/interactions/")

        msg, eph = slash(
            interaction_json={"data": {"name": "leaders"}},
            request=request,
        )
        self.assertIn("Leaders", msg)

    def test_slash_raises_for_unknown_command(self):
        from apps.discord.interactions.handlers.slash import slash

        factory = RequestFactory()
        request = factory.post("/discord/interactions/")

        with self.assertRaises(LookupError):
            slash(
                interaction_json={"data": {"name": "__nonexistent__"}},
                request=request,
            )
