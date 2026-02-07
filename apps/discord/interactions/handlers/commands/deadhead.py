from apps.players.models.player import Player

from .base import SlashCommand


class DeadheadCommand(SlashCommand):
    """Show the player with the most total deaths."""

    name = "deadhead"
    ephemeral = False

    def handle(self) -> tuple[str, bool]:
        player = Player.objects.order_by("-statistics__total_deaths").first()
        url = f"<{self.base_url()}{player.get_absolute_url()}>"
        deaths = player.statistics.total_deaths
        return (
            f"[{player.name}]({url}) :skull_crossbones: {deaths} deaths!",
            self.ephemeral,
        )
