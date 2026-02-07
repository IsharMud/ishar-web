"""Tests for the Discord interactions view.

These tests verify the HTTP-level behaviour: CSRF exemption, signature
verification dispatch, PING/PONG handling, slash-command routing, and
error handling.
"""

import json
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from apps.discord.views import (
    FLAG_EPHEMERAL,
    INTERACTION_APPLICATION_COMMAND,
    INTERACTION_PING,
    RESPONSE_CHANNEL_MESSAGE,
    RESPONSE_PONG,
    InteractionsView,
)


class CSRFExemptionTest(SimpleTestCase):
    """The interactions endpoint MUST be CSRF-exempt.

    Discord sends POST requests without Django CSRF tokens.  If CSRF is
    not properly exempted, Django returns 403 and Discord shows
    "The application did not respond."

    Applying ``@csrf_exempt`` directly to ``dispatch()`` does NOT work
    because Django's ``CsrfViewMiddleware`` inspects the outer view
    callable returned by ``as_view()``, not the ``dispatch`` method.
    The correct approach is ``@method_decorator(csrf_exempt, name='dispatch')``
    on the class.
    """

    def test_as_view_has_csrf_exempt_attribute(self):
        """The view function from as_view() must carry csrf_exempt=True."""
        view_func = InteractionsView.as_view()
        self.assertTrue(
            getattr(view_func, "csrf_exempt", False),
            "InteractionsView.as_view() is missing csrf_exempt=True. "
            "Use @method_decorator(csrf_exempt, name='dispatch') on the class.",
        )


class PingPongTest(SimpleTestCase):
    """Discord sends PING (type 1) to validate the endpoint."""

    @patch("apps.discord.views.verify")
    def test_ping_returns_pong(self, mock_verify):
        factory = RequestFactory()
        body = json.dumps({"type": INTERACTION_PING})
        request = factory.post(
            "/discord/interactions/",
            data=body,
            content_type="application/json",
        )
        response = InteractionsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["type"], RESPONSE_PONG)


class SignatureVerificationTest(SimpleTestCase):
    """Verify that bad/missing signatures are rejected."""

    def _post(self, body=b'{"type":1}'):
        factory = RequestFactory()
        return factory.post(
            "/discord/interactions/",
            data=body,
            content_type="application/json",
        )

    @patch("apps.discord.views.verify", side_effect=ValueError("missing"))
    def test_missing_signature_returns_400(self, _):
        response = InteractionsView.as_view()(self._post())
        self.assertEqual(response.status_code, 400)

    @patch("apps.discord.views.verify")
    def test_bad_signature_returns_401(self, mock_verify):
        from nacl.exceptions import BadSignatureError

        mock_verify.side_effect = BadSignatureError("bad")
        response = InteractionsView.as_view()(self._post())
        self.assertEqual(response.status_code, 401)


class SlashCommandDispatchTest(SimpleTestCase):
    """Test that slash commands are dispatched and responses formatted."""

    def _post_command(self, command_name):
        body = json.dumps({
            "type": INTERACTION_APPLICATION_COMMAND,
            "data": {"name": command_name},
        })
        factory = RequestFactory()
        return factory.post(
            "/discord/interactions/",
            data=body,
            content_type="application/json",
        )

    @patch("apps.discord.views.slash", return_value=("Hello!", False))
    @patch("apps.discord.views.verify")
    def test_public_response(self, _verify, _slash):
        response = InteractionsView.as_view()(self._post_command("test"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["type"], RESPONSE_CHANNEL_MESSAGE)
        self.assertEqual(data["data"]["content"], "Hello!")
        self.assertNotIn("flags", data["data"])

    @patch("apps.discord.views.slash", return_value=("Secret", True))
    @patch("apps.discord.views.verify")
    def test_ephemeral_response(self, _verify, _slash):
        response = InteractionsView.as_view()(self._post_command("test"))
        data = json.loads(response.content)
        self.assertEqual(data["data"]["flags"], FLAG_EPHEMERAL)

    @patch("apps.discord.views.slash", side_effect=LookupError("nope"))
    @patch("apps.discord.views.verify")
    def test_unknown_command(self, _verify, _slash):
        response = InteractionsView.as_view()(self._post_command("bogus"))
        data = json.loads(response.content)
        self.assertEqual(data["data"]["content"], "Unknown command.")
        self.assertEqual(data["data"]["flags"], FLAG_EPHEMERAL)

    @patch("apps.discord.views.slash", side_effect=RuntimeError("db down"))
    @patch("apps.discord.views.verify")
    def test_command_exception_returns_friendly_error(self, _verify, _slash):
        """Unhandled exceptions in commands should not crash the endpoint."""
        response = InteractionsView.as_view()(self._post_command("broken"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["data"]["content"], "Something went wrong.")
        self.assertEqual(data["data"]["flags"], FLAG_EPHEMERAL)


class UnknownInteractionTest(SimpleTestCase):

    @patch("apps.discord.views.verify")
    def test_unknown_type_returns_400(self, _verify):
        body = json.dumps({"type": 999})
        factory = RequestFactory()
        request = factory.post(
            "/discord/interactions/",
            data=body,
            content_type="application/json",
        )
        response = InteractionsView.as_view()(request)
        self.assertEqual(response.status_code, 400)

    @patch("apps.discord.views.verify")
    def test_only_post_allowed(self, _verify):
        factory = RequestFactory()
        request = factory.get("/discord/interactions/")
        response = InteractionsView.as_view()(request)
        self.assertEqual(response.status_code, 405)
