from django.db.models import F
from django.utils.translation import ngettext

from apps.players.models.player import Player

from .base import SlashCommand


class WhoCommand(SlashCommand):
    """List any online players."""

    name = "who"
    ephemeral = True

    def handle(self) -> tuple[str, bool]:
        playing = Player.objects.filter(
            logon__gte=F("logout"),
            is_deleted=False,
            online__gt=0,
        )
        num_play = playing.count()

        if not num_play:
            return "Sorry - no players online.", True

        label = ngettext(
            singular="player", plural="players", number=num_play,
        )
        who_link = self.site_link(
            f"{num_play} {label}", "who", fragment="who",
        )
        reply = f"{who_link}:\n"

        for num, player in enumerate(playing, start=1):
            reply += (
                f"{num}. {player.name}"
                f" {player.true_level} ({player.remorts})\n"
            )

        return reply, False
