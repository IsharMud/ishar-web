from django.urls import reverse
from django.utils.timesince import timeuntil

from apps.seasons.utils.current import get_current_season


def cycle(request):
    # Show the next challenge cycle time.
    cycle_url = (
        f'<{request.scheme}://{request.get_host()}'
        f'{reverse("challenges")}#cycle>'
    )
    next_cycle_dt = get_current_season().get_next_cycle()
    until_next = timeuntil(next_cycle_dt)

    return (
        f"[Challenges will next cycle]({cycle_url}) in {until_next}"
        " :hourglass_flowing_sand:"
        f" {next_cycle_dt.strftime('%A, %B %d, %Y @ %I:%M:%S %p %Z')}."
    )
