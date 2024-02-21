from django.conf import settings

from ishar.apps.players.models import Player


def deadhead():
    """Player with the highest number of deaths."""
    dead_head = Player.objects.exclude(
        true_level__gte=settings.MIN_IMMORTAL_LEVEL
    ).order_by(
        "-deaths"
    ).first()

    return "%s :skull_crossbones: %i times!" % (
        dead_head.name, dead_head.deaths
    )
