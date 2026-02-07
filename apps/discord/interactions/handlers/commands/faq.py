from .base import SlashCommand


class FaqCommand(SlashCommand):
    """Link to frequently asked questions page."""

    name = "faq"
    ephemeral = False

    def handle(self) -> tuple[str, bool]:
        link = self.site_link(
            "Frequently Asked Questions", "faq", fragment="faq",
        )
        return f":question: {link}", self.ephemeral
