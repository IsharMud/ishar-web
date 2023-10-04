"""
isharmud.com context processors for Django templates.
"""
from ishar.apps.seasons.util import get_current_season
from ishar.apps.events.util import get_global_event_count


def current_season(request):
    """
    Context processor for current Ishar MUD season.
    """
    return {"current_season": get_current_season()}


def global_event_count(request):
    """
    Context processor for number of current global events within the MUD.
    """
    return {"global_event_count": get_global_event_count()}
