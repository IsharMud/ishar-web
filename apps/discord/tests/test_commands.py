"""Tests for individual Discord slash command handlers.

All database access and URL resolution is mocked so these tests run
without a database and without URL configuration.
"""

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.test import RequestFactory, SimpleTestCase


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_request():
    """Return a fake Django request that produces a predictable base URL."""
    req = RequestFactory().get("/")
    req.META["SERVER_NAME"] = "isharmud.com"
    req.META["SERVER_PORT"] = "443"
    return req


def _run(cls, interaction_data=None):
    """Execute a command class and return (message, ephemeral)."""
    return cls.execute(
        request=_make_request(),
        interaction_data=interaction_data or {},
    )


# ---------------------------------------------------------------------------
# challenges
# ---------------------------------------------------------------------------

class ChallengesCommandTest(SimpleTestCase):

    @patch("apps.discord.interactions.handlers.commands.challenges.Challenge")
    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/challenges/")
    def test_with_completions(self, _rev, mock_model):
        from apps.discord.interactions.handlers.commands.challenges import (
            ChallengesCommand,
        )
        qs = MagicMock()
        mock_model.objects.filter.return_value = qs
        qs.exclude.return_value.count.return_value = 3
        qs.filter.return_value.count.return_value = 2

        msg, eph = _run(ChallengesCommand)
        self.assertFalse(eph)
        self.assertIn("Challenges", msg)
        self.assertIn("3 complete", msg)
        self.assertIn("2 incomplete", msg)
        self.assertIn(":crossed_swords:", msg)

    @patch("apps.discord.interactions.handlers.commands.challenges.Challenge")
    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/challenges/")
    def test_zero_counts(self, _rev, mock_model):
        from apps.discord.interactions.handlers.commands.challenges import (
            ChallengesCommand,
        )
        qs = MagicMock()
        mock_model.objects.filter.return_value = qs
        qs.exclude.return_value.count.return_value = 0
        qs.filter.return_value.count.return_value = 0

        msg, eph = _run(ChallengesCommand)
        # When count is 0, output is plain text (no link).
        self.assertIn("0 complete", msg)
        self.assertIn("0 incomplete", msg)


# ---------------------------------------------------------------------------
# cycle
# ---------------------------------------------------------------------------

class CycleCommandTest(SimpleTestCase):

    @patch("apps.discord.interactions.handlers.commands.cycle.get_current_season")
    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/challenges/")
    def test_output(self, _rev, mock_season):
        from apps.discord.interactions.handlers.commands.cycle import CycleCommand

        future = datetime.now(timezone.utc) + timedelta(days=3)
        mock_season.return_value.get_next_cycle.return_value = future

        msg, eph = _run(CycleCommand)
        self.assertFalse(eph)
        self.assertIn(":arrows_counterclockwise:", msg)
        self.assertIn("Challenges will next cycle", msg)
        self.assertIn(":hourglass_flowing_sand:", msg)


# ---------------------------------------------------------------------------
# deadhead
# ---------------------------------------------------------------------------

class DeadheadCommandTest(SimpleTestCase):

    @patch("apps.discord.interactions.handlers.commands.deadhead.Player")
    def test_output(self, mock_model):
        from apps.discord.interactions.handlers.commands.deadhead import (
            DeadheadCommand,
        )
        player = SimpleNamespace(
            name="Grim",
            get_absolute_url=lambda: "/player/Grim/",
            statistics=SimpleNamespace(total_deaths=999),
        )
        mock_model.objects.order_by.return_value.first.return_value = player

        msg, eph = _run(DeadheadCommand)
        self.assertFalse(eph)
        self.assertIn("Grim", msg)
        self.assertIn("999 deaths", msg)
        self.assertIn(":skull_crossbones:", msg)


# ---------------------------------------------------------------------------
# events
# ---------------------------------------------------------------------------

class EventsCommandTest(SimpleTestCase):

    @patch("apps.discord.interactions.handlers.commands.events.GlobalEvent")
    @patch("apps.discord.interactions.handlers.commands.events.now")
    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/events/")
    def test_no_events(self, _rev, mock_now, mock_model):
        from apps.discord.interactions.handlers.commands.events import (
            EventsCommand,
        )
        mock_now.return_value = datetime.now(timezone.utc)
        mock_model.objects.filter.return_value.count.return_value = 0

        msg, eph = _run(EventsCommand)
        self.assertTrue(eph)
        self.assertIn("no events", msg)

    @patch("apps.discord.interactions.handlers.commands.events.GlobalEvent")
    @patch("apps.discord.interactions.handlers.commands.events.now")
    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/events/")
    def test_with_events(self, _rev, mock_now, mock_model):
        from apps.discord.interactions.handlers.commands.events import (
            EventsCommand,
        )
        utc_now = datetime.now(timezone.utc)
        mock_now.return_value = utc_now

        event = SimpleNamespace(
            event_desc="Double XP",
            end_time=utc_now + timedelta(hours=6),
        )
        qs = MagicMock()
        mock_model.objects.filter.return_value = qs
        qs.count.return_value = 1
        qs.__iter__ = MagicMock(return_value=iter([event]))

        msg, eph = _run(EventsCommand)
        self.assertFalse(eph)
        self.assertIn("1 event", msg)
        self.assertIn("Double XP", msg)
        self.assertIn(":alarm_clock:", msg)


# ---------------------------------------------------------------------------
# faq
# ---------------------------------------------------------------------------

class FaqCommandTest(SimpleTestCase):

    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/faq/")
    def test_output(self, _rev):
        from apps.discord.interactions.handlers.commands.faq import FaqCommand

        msg, eph = _run(FaqCommand)
        self.assertFalse(eph)
        self.assertIn(":question:", msg)
        self.assertIn("Frequently Asked Questions", msg)


# ---------------------------------------------------------------------------
# feedback
# ---------------------------------------------------------------------------

class FeedbackCommandTest(SimpleTestCase):

    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/feedback/")
    def test_output(self, _rev):
        from apps.discord.interactions.handlers.commands.feedback import (
            FeedbackCommand,
        )
        msg, eph = _run(FeedbackCommand)
        self.assertFalse(eph)
        self.assertIn(":mailbox_with_mail:", msg)
        self.assertIn("Feedback", msg)


# ---------------------------------------------------------------------------
# leader
# ---------------------------------------------------------------------------

class LeaderCommandTest(SimpleTestCase):

    @patch("apps.discord.interactions.handlers.commands.leader.Leader")
    @patch("apps.discord.interactions.handlers.commands.leader.settings")
    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/leaders/")
    def test_default_leader(self, _rev, mock_settings, mock_model):
        from apps.discord.interactions.handlers.commands.leader import (
            LeaderCommand,
        )
        mock_settings.WEBSITE_TITLE = "Ishar MUD"
        player = SimpleNamespace(name="Hero")
        mock_model.objects.first.return_value = player

        msg, eph = _run(LeaderCommand)
        self.assertFalse(eph)
        self.assertIn(":trophy:", msg)
        self.assertIn("Hero", msg)
        self.assertIn("Ishar MUD leader", msg)

    @patch("apps.discord.interactions.handlers.commands.leader.GameType")
    @patch("apps.discord.interactions.handlers.commands.leader.Leader")
    @patch("apps.discord.interactions.handlers.commands.leader.settings")
    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/leaders/hardcore/")
    def test_with_game_type(self, _rev, mock_settings, mock_model, mock_gt):
        from apps.discord.interactions.handlers.commands.leader import (
            LeaderCommand,
        )
        mock_settings.WEBSITE_TITLE = "Ishar MUD"
        game_type_inst = MagicMock()
        game_type_inst.value = 1
        game_type_inst.label = "Hardcore"
        mock_gt.return_value = game_type_inst

        player = SimpleNamespace(name="Tank")
        mock_model.objects.filter.return_value.first.return_value = player

        data = {"options": [{"name": "type", "value": "1"}]}
        msg, eph = _run(LeaderCommand, interaction_data=data)
        self.assertIn("Tank", msg)
        self.assertIn("Hardcore leader", msg)


# ---------------------------------------------------------------------------
# leaders
# ---------------------------------------------------------------------------

class LeadersCommandTest(SimpleTestCase):

    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/leaders/")
    def test_output(self, _rev):
        from apps.discord.interactions.handlers.commands.leaders import (
            LeadersCommand,
        )
        msg, eph = _run(LeadersCommand)
        self.assertFalse(eph)
        self.assertIn(":trophy:", msg)
        self.assertIn("Leaders", msg)


# ---------------------------------------------------------------------------
# mudhelp + spell
# ---------------------------------------------------------------------------

class MudhelpCommandTest(SimpleTestCase):

    @patch("apps.discord.interactions.handlers.commands.mudhelp.HelpTab")
    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/help/")
    def test_no_results(self, _rev, mock_helptab):
        from apps.discord.interactions.handlers.commands.mudhelp import (
            MudhelpCommand,
        )
        mock_helptab.return_value.search.return_value = {}
        data = {"options": [{"name": "topic", "value": "nonexistent"}]}

        msg, eph = _run(MudhelpCommand, interaction_data=data)
        self.assertTrue(eph)
        self.assertIn("no such help topic", msg)

    @patch("apps.discord.interactions.handlers.commands.mudhelp.HelpTab")
    @patch("apps.discord.interactions.handlers.commands.mudhelp.reverse",
           return_value="/help/fireball/")
    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/help/fireball/")
    def test_single_result(self, _rev1, _rev2, mock_helptab):
        from apps.discord.interactions.handlers.commands.mudhelp import (
            MudhelpCommand,
        )
        topic = SimpleNamespace(
            name="Fireball",
            get_absolute_url=lambda: "/help/fireball/",
        )
        mock_helptab.return_value.search.return_value = {"fireball": topic}
        data = {"options": [{"name": "topic", "value": "fireball"}]}

        msg, eph = _run(MudhelpCommand, interaction_data=data)
        self.assertFalse(eph)
        self.assertIn(":information_source:", msg)
        self.assertIn("Fireball", msg)

    @patch("apps.discord.interactions.handlers.commands.mudhelp.HelpTab")
    @patch("apps.discord.interactions.handlers.commands.mudhelp.reverse",
           return_value="/help/fire/")
    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/help/fire/")
    def test_multiple_results(self, _rev1, _rev2, mock_helptab):
        from apps.discord.interactions.handlers.commands.mudhelp import (
            MudhelpCommand,
        )
        results = {
            "fireball": SimpleNamespace(name="Fireball"),
            "fire shield": SimpleNamespace(name="Fire Shield"),
        }
        mock_helptab.return_value.search.return_value = results
        data = {"options": [{"name": "topic", "value": "fire"}]}

        msg, eph = _run(MudhelpCommand, interaction_data=data)
        self.assertFalse(eph)
        self.assertIn("2 results", msg)

    @patch("apps.discord.interactions.handlers.commands.mudhelp.HelpTab")
    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/help/")
    def test_missing_option(self, _rev, mock_helptab):
        from apps.discord.interactions.handlers.commands.mudhelp import (
            MudhelpCommand,
        )
        msg, eph = _run(MudhelpCommand, interaction_data={})
        self.assertTrue(eph)
        self.assertIn("no such help topic", msg)


class SpellCommandTest(SimpleTestCase):

    @patch("apps.discord.interactions.handlers.commands.mudhelp.HelpTab")
    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/help/")
    def test_spell_not_found(self, _rev, mock_helptab):
        from apps.discord.interactions.handlers.commands.mudhelp import (
            SpellCommand,
        )
        mock_helptab.return_value.search.return_value = {}
        data = {"options": [{"name": "spell", "value": "nope"}]}

        msg, eph = _run(SpellCommand, interaction_data=data)
        self.assertTrue(eph)
        self.assertIn("no such spell", msg)

    @patch("apps.discord.interactions.handlers.commands.mudhelp.HelpTab")
    @patch("apps.discord.interactions.handlers.commands.mudhelp.reverse",
           return_value="/help/fireball/")
    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/help/fireball/")
    def test_spell_found(self, _rev1, _rev2, mock_helptab):
        from apps.discord.interactions.handlers.commands.mudhelp import (
            SpellCommand,
        )
        topic = SimpleNamespace(
            name="Fireball",
            get_absolute_url=lambda: "/help/fireball/",
        )
        mock_helptab.return_value.search.return_value = {"fireball": topic}
        data = {"options": [{"name": "spell", "value": "fireball"}]}

        msg, eph = _run(SpellCommand, interaction_data=data)
        self.assertFalse(eph)
        self.assertIn("Fireball", msg)


# ---------------------------------------------------------------------------
# mudtime
# ---------------------------------------------------------------------------

class MudtimeCommandTest(SimpleTestCase):

    @patch("apps.discord.interactions.handlers.commands.mudtime.now")
    def test_output(self, mock_now):
        from apps.discord.interactions.handlers.commands.mudtime import (
            MudtimeCommand,
        )
        mock_now.return_value = datetime(
            2025, 6, 15, 12, 30, 0, tzinfo=timezone.utc,
        )
        msg, eph = _run(MudtimeCommand)
        self.assertFalse(eph)
        self.assertIn("Sunday", msg)
        self.assertIn("June", msg)
        self.assertIn(":clock:", msg)


# ---------------------------------------------------------------------------
# runtime
# ---------------------------------------------------------------------------

class RuntimeCommandTest(SimpleTestCase):

    @patch("apps.discord.interactions.handlers.commands.runtime.get_process")
    def test_output(self, mock_proc):
        from apps.discord.interactions.handlers.commands.runtime import (
            RuntimeCommand,
        )
        created = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        mock_proc.return_value = SimpleNamespace(
            created=created,
            runtime=lambda: "5 days",
        )
        msg, eph = _run(RuntimeCommand)
        self.assertFalse(eph)
        self.assertIn("Running since", msg)
        self.assertIn("5 days", msg)
        self.assertIn(":clock:", msg)


# ---------------------------------------------------------------------------
# season
# ---------------------------------------------------------------------------

class SeasonCommandTest(SimpleTestCase):

    @patch("apps.discord.interactions.handlers.commands.season.get_current_season")
    def test_output(self, mock_season):
        from apps.discord.interactions.handlers.commands.season import (
            SeasonCommand,
        )
        expires = datetime.now(timezone.utc) + timedelta(days=30)
        mock_season.return_value = SimpleNamespace(
            season_id=42,
            expiration_date=expires,
            get_absolute_url=lambda: "/season/42/",
        )
        msg, eph = _run(SeasonCommand)
        self.assertFalse(eph)
        self.assertIn("Season 42", msg)
        self.assertIn(":hourglass_flowing_sand:", msg)
        self.assertIn(":alarm_clock:", msg)


# ---------------------------------------------------------------------------
# upgrades
# ---------------------------------------------------------------------------

class UpgradesCommandTest(SimpleTestCase):

    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/upgrades/")
    def test_output(self, _rev):
        from apps.discord.interactions.handlers.commands.upgrades import (
            UpgradesCommand,
        )
        msg, eph = _run(UpgradesCommand)
        self.assertFalse(eph)
        self.assertIn(":shield:", msg)
        self.assertIn("Remort Upgrades", msg)


# ---------------------------------------------------------------------------
# who
# ---------------------------------------------------------------------------

class WhoCommandTest(SimpleTestCase):

    @patch("apps.discord.interactions.handlers.commands.who.Player")
    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/who/")
    def test_no_players(self, _rev, mock_model):
        from apps.discord.interactions.handlers.commands.who import WhoCommand

        mock_model.objects.filter.return_value.count.return_value = 0

        msg, eph = _run(WhoCommand)
        self.assertTrue(eph)
        self.assertIn("no players online", msg)

    @patch("apps.discord.interactions.handlers.commands.who.Player")
    @patch("apps.discord.interactions.handlers.commands.base.reverse",
           return_value="/who/")
    def test_with_players(self, _rev, mock_model):
        from apps.discord.interactions.handlers.commands.who import WhoCommand

        players = [
            SimpleNamespace(name="Warrior", true_level=30, remorts=5),
            SimpleNamespace(name="Mage", true_level=20, remorts=2),
        ]
        qs = MagicMock()
        mock_model.objects.filter.return_value = qs
        qs.count.return_value = 2
        qs.__iter__ = MagicMock(return_value=iter(players))

        msg, eph = _run(WhoCommand)
        self.assertFalse(eph)
        self.assertIn("2 players", msg)
        self.assertIn("Warrior", msg)
        self.assertIn("Mage", msg)
        self.assertIn("30", msg)
        self.assertIn("(5)", msg)
