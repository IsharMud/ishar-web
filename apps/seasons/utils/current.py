from ..models.season import Season


def get_current_season():
    # Get the current, latest, active Ishar MUD season.
    return Season.objects.latest()

async def aget_current_season():
    # Asynchronously get the current, latest, active Ishar MUD season.
    return Season.objects.alatest()
