from django.utils.timesince import timeuntil

from ishar.apps.seasons.models import Season

from ..response import respond


def season() -> respond:
    """Show current season number, expiration, and time until expiration."""
    current_season = Season.objects.filter(is_active=1).first()

    return respond(
        "Season %i :hourglass_flowing_sand: ends %s :alarm_clock: %s." % (
            current_season.season_id,
            timeuntil(current_season.expiration_date),
            current_season.expiration_date
        )
    )
