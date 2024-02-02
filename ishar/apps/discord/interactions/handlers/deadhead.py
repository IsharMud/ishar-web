from django.conf import settings

from ishar.apps.players.models import Player

from ..response import respond


def deadhead() -> respond:
    """Player with the highest number of deaths."""
    dead_head = Player.objects.filter(
        true_level__lt=min(settings.IMMORTAL_LEVELS)[0],
    ).order_by("-deaths").first()

    return respond(
        "%s :skull_crossbones: %i times!" % (dead_head.name, dead_head.deaths)
    )
