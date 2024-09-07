from apps.players.models.player import Player


def deadhead():
    """Player with the highest number of total deaths."""
    dead_head = Player.objects.order_by("-statistics__total_deaths").first()
    return "%s :skull_crossbones: %i total deaths!" % (
        dead_head.name,
        dead_head.statistics.total_deaths
    )
