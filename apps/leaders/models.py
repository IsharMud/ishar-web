from apps.players.models.player import Player


class Leader(Player):
    """Ishar leader."""

    class Meta:
        # Re-order proxy model of Player.
        ordering = (
            "-remorts",
            "-statistics__total_renown",
            "-statistics__total_challenges",
            "-statistics__total_quests",
            "statistics__total_deaths",
            "-common__level",
        )
        proxy = True
