from django.core.cache import cache

from ..models.season import Season


def _get_current_season():
    # Get the current, latest, active Ishar MUD season.
    return Season.objects.latest()


def get_current_season():
    # Cache the current, latest, active Ishar MUD season.
    return cache.get_or_set("current_season", _get_current_season)
