from django.utils.timesince import timeuntil

from apps.seasons.utils.current import get_current_season

from .base import SlashCommand


class CycleCommand(SlashCommand):
    """Show when challenges will cycle next."""

    name = "cycle"
    ephemeral = False

    def handle(self) -> tuple[str, bool]:
        next_cycle_dt = get_current_season().get_next_cycle()
        cycle_link = self.site_link(
            "Challenges will next cycle", "challenges", fragment="cycle",
        )
        timestamp = next_cycle_dt.strftime("%A, %B %d, %Y @ %I:%M:%S %p %Z")

        return (
            f":arrows_counterclockwise: {cycle_link}"
            f" in {timeuntil(next_cycle_dt)}"
            f" :hourglass_flowing_sand: {timestamp}.",
            self.ephemeral,
        )
