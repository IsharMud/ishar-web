from django.core.cache import cache

from ..models.season import Season


def _get_current_season():
    # Current Ishar MUD season.
    season = Season.objects.filter(
        is_active=1,
        # effective_date__gt=timezone.now(),
        # expiration_date__lt=timezone.now()
    ).first()
    return season


def get_current_season():
    return cache.get_or_set("current_season", _get_current_season)
