from .base import SlashCommand


class FeedbackCommand(SlashCommand):
    """Link to feedback page."""

    name = "feedback"
    ephemeral = False

    def handle(self) -> tuple[str, bool]:
        link = self.site_link("Feedback", "feedback", fragment="feedback")
        return f":mailbox_with_mail: {link}", self.ephemeral
