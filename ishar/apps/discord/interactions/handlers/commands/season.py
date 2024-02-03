from django.utils.timesince import timeuntil

from ishar.apps.seasons.models import Season


def season():
    """Show current season number, expiration, and time until expiration."""
    current_season = Season.objects.filter(is_active=1).first()
    dt_fmt = "%A, %B %d, %Y @ %I:%M:%S %p %Z"

    return (
        "Season %i :hourglass_flowing_sand: ends %s :alarm_clock: %s." % (
            current_season.season_id,
            timeuntil(current_season.expiration_date),
            current_season.expiration_date.strftime(dt_fmt)
        )
    )
