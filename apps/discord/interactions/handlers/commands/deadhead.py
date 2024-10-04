from apps.players.models.player import Player


def deadhead(request):
    # Player with the highest number of total deaths.
    who = Player.objects.order_by("-statistics__total_deaths").first()
    url = f"<{request.scheme}://{request.get_host()}{who.get_absolute_url()}>"
    deaths = who.statistics.total_deaths
    return (
        f"[{who.name}]({url}) :skull_crossbones: {deaths} deaths!"
    )
