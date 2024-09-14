from apps.players.models.player import Player


def deadhead():
    """Player with the highest number of total deaths."""
    dh = Player.objects.order_by("-statistics__total_deaths").first()
    return f"{dh.name} :skull_crossbones: {dh.statistics.total_deaths} deaths!"
