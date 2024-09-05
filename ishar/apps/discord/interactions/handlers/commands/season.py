from django.urls import reverse
from django.utils.timesince import timeuntil

from ishar.apps.seasons.utils.current import get_current_season


def season(request):
    """Current season number, expiration, time until expiration, and URL."""
    current_season = get_current_season()
    current_season_url = "%s://%s%s#%s" % (
        request.scheme, request.get_host(), reverse("current_season"), "season"
    )
    dt_fmt = "%A, %B %d, %Y @ %I:%M:%S %p %Z"

    return (
        "Season %i :hourglass_flowing_sand: ends %s :alarm_clock: %s <%s>" % (
            current_season.season_id,
            timeuntil(current_season.expiration_date),
            current_season.expiration_date.strftime(dt_fmt),
            current_season_url
        )
    )
