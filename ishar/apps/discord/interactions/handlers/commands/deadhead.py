from django.conf import settings

from ishar.apps.players.models.player import Player


def deadhead():
    """Player with the highest number of total deaths."""
    dead_head = Player.objects.exclude(
        true_level__gte=settings.MIN_IMMORTAL_LEVEL
    ).order_by(
        "-statistics__total_deaths"
    ).first()

    return "%s :skull_crossbones: %i total deaths!" % (
        dead_head.name,
        dead_head.statistics.total_deaths
    )
