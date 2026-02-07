from apps.processes.utils.process import get_process

from .base import SlashCommand


class RuntimeCommand(SlashCommand):
    """Show the current server process runtime."""

    name = "runtime"
    ephemeral = False

    def handle(self) -> tuple[str, bool]:
        process = get_process()
        timestamp = process.created.strftime(
            "%A, %B %d, %Y @ %I:%M:%S %p %Z"
        )
        return (
            f"Running since {timestamp} ({process.runtime()}) :clock:",
            self.ephemeral,
        )
