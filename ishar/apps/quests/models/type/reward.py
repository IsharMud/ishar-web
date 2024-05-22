from django.db.models import IntegerChoices


class QuestRewardType(IntegerChoices):
    """Quest reward type choices."""
    NEGATIVE_ONE = -1
    OBJECT_ALWAYS = 0, "Object (Always)"
    OBJECT_CHOICE = 1, "Object (Choice)"
    MONEY = 2
    ALIGNMENT = 3
    SKILL = 4
    RENOWN = 5
    EXPERIENCE = 6
    QUEST = 7
    RELIC = 8

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.value
        )

    def __str__(self) -> str:
        return self.name.title()
