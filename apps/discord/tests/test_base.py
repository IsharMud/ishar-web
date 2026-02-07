"""Tests for the SlashCommand base class and auto-registration registry."""

from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from apps.discord.interactions.handlers.commands.base import (
    SlashCommand,
    _registry,
    get_all_commands,
    get_command,
)


class RegistryTest(SimpleTestCase):
    """Verify that subclassing SlashCommand registers commands."""

    def test_base_class_not_registered(self):
        """SlashCommand itself has name='' and should not be registered."""
        self.assertNotIn("", _registry)

    def test_named_subclass_is_registered(self):
        """A subclass with a name should appear in the registry."""

        class _DummyCmd(SlashCommand):
            name = "_test_registry_dummy"

            def handle(self):
                return "ok", True

        self.assertIs(get_command("_test_registry_dummy"), _DummyCmd)

    def test_unnamed_subclass_not_registered(self):
        """A subclass without a name should not be registered."""

        class _NoNameCmd(SlashCommand):
            pass

        self.assertIsNone(get_command(""))

    def test_get_all_commands_returns_copy(self):
        """get_all_commands() returns a dict that won't mutate the real one."""
        copy = get_all_commands()
        copy["__bogus__"] = None
        self.assertNotIn("__bogus__", _registry)

    def test_all_expected_commands_registered(self):
        """Ensure all 15 slash commands from the YAML are registered."""
        # Import triggers registration.
        import apps.discord.interactions.handlers.commands  # noqa: F401

        expected = {
            "challenges", "cycle", "deadhead", "events", "faq",
            "feedback", "leader", "leaders", "mudhelp", "mudtime",
            "runtime", "season", "spell", "upgrades", "who",
        }
        self.assertTrue(
            expected.issubset(_registry.keys()),
            f"Missing commands: {expected - _registry.keys()}",
        )


class SlashCommandHelpersTest(SimpleTestCase):
    """Test the helper methods on SlashCommand instances."""

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/")
        # RequestFactory doesn't populate scheme, so set explicitly.
        self.request.META["SERVER_NAME"] = "isharmud.com"
        self.request.META["SERVER_PORT"] = "443"

    def _make_cmd(self, **kwargs):
        """Create a bare SlashCommand with the given init kwargs."""

        class _Cmd(SlashCommand):
            # No name so it doesn't pollute the registry.
            def handle(self):
                return "test", True

        return _Cmd(**kwargs)

    def test_base_url_with_request(self):
        cmd = self._make_cmd(request=self.request)
        url = cmd.base_url()
        self.assertIn("isharmud.com", url)

    def test_base_url_without_request(self):
        cmd = self._make_cmd()
        self.assertEqual(cmd.base_url(), "")

    @patch("apps.discord.interactions.handlers.commands.base.reverse")
    def test_site_url_without_fragment(self, mock_reverse):
        mock_reverse.return_value = "/challenges/"
        cmd = self._make_cmd(request=self.request)
        url = cmd.site_url("challenges")
        self.assertIn("/challenges/", url)
        self.assertNotIn("#", url)

    @patch("apps.discord.interactions.handlers.commands.base.reverse")
    def test_site_url_with_fragment(self, mock_reverse):
        mock_reverse.return_value = "/challenges/"
        cmd = self._make_cmd(request=self.request)
        url = cmd.site_url("challenges", fragment="cycle")
        self.assertTrue(url.endswith("#cycle"))

    @patch("apps.discord.interactions.handlers.commands.base.reverse")
    def test_site_link_format(self, mock_reverse):
        mock_reverse.return_value = "/faq/"
        cmd = self._make_cmd(request=self.request)
        link = cmd.site_link("FAQ", "faq", fragment="faq")
        self.assertTrue(link.startswith("[FAQ]"))
        self.assertIn("#faq", link)
        # Discord suppressed-embed format: [label](<url>)
        self.assertIn("(<", link)
        self.assertIn(">)", link)

    def test_get_option_found(self):
        data = {"options": [{"name": "type", "value": "1"}]}
        cmd = self._make_cmd(interaction_data=data)
        self.assertEqual(cmd.get_option("type"), "1")

    def test_get_option_missing(self):
        cmd = self._make_cmd(interaction_data={})
        self.assertIsNone(cmd.get_option("type"))

    def test_get_option_default(self):
        cmd = self._make_cmd(interaction_data={})
        self.assertEqual(cmd.get_option("type", "fallback"), "fallback")

    def test_get_options_empty(self):
        cmd = self._make_cmd(interaction_data={})
        self.assertEqual(cmd.get_options(), [])

    def test_handle_raises_not_implemented(self):
        """The base handle() should raise NotImplementedError."""
        cmd = SlashCommand()
        with self.assertRaises(NotImplementedError):
            cmd.handle()

    def test_execute_classmethod(self):
        """execute() should instantiate and call handle()."""

        class _EchoCmd(SlashCommand):
            def handle(self):
                return "echo", False

        msg, eph = _EchoCmd.execute()
        self.assertEqual(msg, "echo")
        self.assertFalse(eph)
