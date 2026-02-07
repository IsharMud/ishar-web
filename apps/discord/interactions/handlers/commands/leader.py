from django.conf import settings

from apps.leaders.models import Leader
from apps.players.models.game_type import GameType

from .base import SlashCommand


class LeaderCommand(SlashCommand):
    """Show the leading player, optionally filtered by game type."""

    name = "leader"
    ephemeral = False

    def handle(self) -> tuple[str, bool]:
        label = settings.WEBSITE_TITLE
        view_name = "leaders"
        fragment = "leaders"
        qs = Leader.objects

        game_type_value = self.get_option("type")
        if game_type_value is not None:
            game_type = GameType(int(game_type_value))
            qs = qs.filter(game_type__exact=game_type.value)
            label = game_type.label
            view_name = f"{label.lower()}_leaders"
            fragment = label.lower()

        lead_player = qs.first()
        link = self.site_link(f"{label} leader", view_name, fragment=fragment)
        return (
            f":trophy: {lead_player.name} is the {link}!",
            self.ephemeral,
        )
