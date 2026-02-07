from apps.challenges.models import Challenge

from .base import SlashCommand


class ChallengesCommand(SlashCommand):
    """Link to challenges page with counts of active, complete, incomplete."""

    name = "challenges"
    ephemeral = False

    def handle(self) -> tuple[str, bool]:
        active = Challenge.objects.filter(is_active__exact=1)
        num_complete = active.exclude(winner_desc__exact="").count()
        num_incomplete = active.filter(winner_desc__exact="").count()

        challenges_link = self.site_link(
            "Challenges", "challenges", fragment="challenges",
        )

        if num_complete:
            complete = self.site_link(
                f"{num_complete} complete", "complete", fragment="complete",
            )
        else:
            complete = f"{num_complete} complete"

        if num_incomplete:
            incomplete = self.site_link(
                f"{num_incomplete} incomplete",
                "incomplete",
                fragment="incomplete",
            )
        else:
            incomplete = f"{num_incomplete} incomplete"

        return (
            f"{challenges_link} :crossed_swords: {complete} - {incomplete}.",
            self.ephemeral,
        )
