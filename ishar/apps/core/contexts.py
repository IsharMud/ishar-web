"""
isharmud.com context processors for Django templates.
"""
from django.conf import settings

from ishar.apps.seasons.util import get_current_season
from ishar.apps.events.util import get_global_event_count


def current_season(request):
    """
    Context processor for current Ishar MUD season.
    """
    return {"CURRENT_SEASON": get_current_season()}


def global_event_count(request):
    """
    Context processor for number of current global events within the MUD.
    """
    return {"GLOBAL_EVENT_COUNT": get_global_event_count()}


def website_title(request):
    """
    Context processor for website title.
    """
    return {"WEBSITE_TITLE": settings.WEBSITE_TITLE}
