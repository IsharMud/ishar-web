from django.utils.timesince import timeuntil

from apps.seasons.utils.current import get_current_season


def cycle():
    """Show the next challenge cycle time."""
    next_cycle = get_current_season().get_next_cycle()
    return "Challenges will next cycle in %s :hourglass_flowing_sand: %s" % (
        timeuntil(next_cycle),
        next_cycle.strftime("%A, %B %d, %Y @ %I:%M:%S %p %Z"),
    )
