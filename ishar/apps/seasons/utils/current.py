from ..models.season import Season


def get_current_season():
    """Current Ishar MUD season."""
    season = Season.objects.filter(
        is_active=1,
        # effective_date__gt=timezone.now(),
        # expiration_date__lt=timezone.now()
    ).first()
    return season
