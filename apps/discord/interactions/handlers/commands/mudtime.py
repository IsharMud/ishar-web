from django.utils.timezone import now

from .base import SlashCommand


class MudtimeCommand(SlashCommand):
    """Show the current server (UTC) time."""

    name = "mudtime"
    ephemeral = False

    def handle(self) -> tuple[str, bool]:
        timestamp = now().strftime("%A, %B %d, %Y @ %I:%M:%S %p %Z")
        return f"{timestamp} :clock:", self.ephemeral
