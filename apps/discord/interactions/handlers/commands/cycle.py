from django.utils.timesince import timeuntil

from apps.seasons.utils.current import get_current_season


def cycle():
    """Show the next challenge cycle time."""
    next_cycle_dt = get_current_season().get_next_cycle()
    until_next = timeuntil(next_cycle_dt)
    return (
        f'Challenges will next cycle in {until_next} :hourglass_flowing_sand:'
        f' {next_cycle_dt.strftime("%A, %B %d, %Y @ %I:%M:%S %p %Z")}.'
    )
