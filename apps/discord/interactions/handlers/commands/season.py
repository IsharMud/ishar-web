from django.utils.timesince import timeuntil

from apps.seasons.utils.current import get_current_season

from .base import SlashCommand

DT_FMT = "%A, %B %d, %Y @ %I:%M:%S %p %Z"


class SeasonCommand(SlashCommand):
    """Show the current season number and expiration."""

    name = "season"
    ephemeral = False

    def handle(self) -> tuple[str, bool]:
        current = get_current_season()
        url = f"<{self.base_url()}{current.get_absolute_url()}>"
        expires = current.expiration_date
        return (
            f"[Season {current.season_id}]({url})"
            f" :hourglass_flowing_sand: ends {timeuntil(expires)}"
            f" :alarm_clock: {expires.strftime(DT_FMT)}",
            self.ephemeral,
        )
