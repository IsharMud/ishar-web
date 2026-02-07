from .base import SlashCommand


class UpgradesCommand(SlashCommand):
    """Link to remort upgrades page."""

    name = "upgrades"
    ephemeral = False

    def handle(self) -> tuple[str, bool]:
        link = self.site_link(
            "Remort Upgrades", "upgrades", fragment="upgrades",
        )
        return f":shield: {link}", self.ephemeral
