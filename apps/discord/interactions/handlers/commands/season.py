from django.utils.timesince import timeuntil

from apps.seasons.utils.current import get_current_season


def season(request):
    # Current season number, expiration, time until expiration, and URL.
    current_season = get_current_season()
    dt_fmt = "%A, %B %d, %Y @ %I:%M:%S %p %Z"

    return (
        f'[Season {current_season.season_id}]'
        f'(<{request.scheme}://{request.get_host()}'
        f'{current_season.get_absolute_url()}>) :hourglass_flowing_sand:'
        f' ends {timeuntil(current_season.expiration_date)} :alarm_clock:'
        f' {current_season.expiration_date.strftime(dt_fmt)}'
    )
