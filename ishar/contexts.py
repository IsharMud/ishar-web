"""
isharmud.com context processors for Django templates.
"""
from ishar.apps.events.models import GlobalEvent
from ishar.apps.season.models import Season


def current_season(request):
    """
    Current Ishar MUD season.
    """
    return {"current_season": Season.objects.filter(is_active=1).first()}


def global_event_count(request):
    """
    Number of current global events within the MUD.
    """
    return {"global_event_count": GlobalEvent.objects.filter(is_active=1).first()}
