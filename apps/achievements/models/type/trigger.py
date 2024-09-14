from django.db.models import IntegerChoices


class AchievementTriggerType(IntegerChoices):
    """Achievement trigger type choices."""
    NONE = 0
    LEVEL_UP = 1
    REMORT = 2
    GAIN_RENOWN = 3
    DEATH = 4
    QUEST_COMPLETE = 5
    CHALLENGE_COMPLETE = 6
    MAX_TRIGGER = 7

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.value})"

    def __str__(self) -> str:
        return self.name.title()
