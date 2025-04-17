from django.urls import reverse
from django.db.models.expressions import F
from django.utils.translation import ngettext

from apps.players.models.player import Player


def who(request):
    # List any online players.

    # Default message assuming there are no active events.
    ephemeral = True
    reply = "Sorry - no players online."

    # Find the online players in the database.
    playing = Player.objects.filter(
        logon__gte=F("logout"),
        is_deleted=False,
        online__gt=0
    )

    # Proceed if there are any players online.
    num_play = playing.count()
    if num_play and num_play > 0:
        ephemeral = False
        reply = (
            f'[{num_play} '
            f'{ngettext(singular="player", plural="players", number=num_play)}]'
            f'(<{request.scheme}://{request.get_host()}'
            f'{reverse("who")}#who>):\n'
        )

        # List the name, level, and number of remorts for each player online.
        for num, player in enumerate(playing.all(), start=1):
            reply += (
                f"{num}. {player.name} {player.true_level} ({player.remorts})"
            )

    # Return the reply.
    return reply, ephemeral
