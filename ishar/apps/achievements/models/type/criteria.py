from django.db.models import TextChoices


class AchievementCriteriaType(TextChoices):
    """Achievement criteria type choices."""
    PLAYER_ONLY = "PlayerOnly", "Player Only"
    ACCOUNT = "Account"
    ACCOUNT_GROUPED = "AccountGrouped", "Account (Grouped)"
    ACCOUNT_TOTAL = "AccountTotal", "Account (Total)"

    def __repr__(self) -> str:
        return "%s: %s (%s)" % (
            self.__class__.__name__,
            self.__str__(),
            self.name
        )

    def __str__(self) -> str:
        return self.value
