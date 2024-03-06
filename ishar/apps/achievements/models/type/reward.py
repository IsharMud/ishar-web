from django.db.models import IntegerChoices


class AchievementRewardType(IntegerChoices):
    """
    Achievement reward types.
    """
    NEGATIVE_ONE = -1
    ACHIEVEMENT_POINTS = 0
    ESSENCE = 1
    SOULBOUND_ITEM = 2
    TITLE = 3

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.value
        )

    def __str__(self) -> str:
        return self.name
