from .base import SlashCommand


class LeadersCommand(SlashCommand):
    """Link to leaders page."""

    name = "leaders"
    ephemeral = False

    def handle(self) -> tuple[str, bool]:
        link = self.site_link("Leaders", "leaders", fragment="leaders")
        return f":trophy: {link}", self.ephemeral
