from django.db.models import IntegerChoices


class QuestRewardType(IntegerChoices):
    """
    Quest reward types.
    """
    NEGATIVE_ONE = -1, "Negative One"
    OBJECT_ALWAYS = 0, "Object (Always)"
    OBJECT_CHOICE = 1, "Object (Choice)"
    MONEY = 2, "Money"
    ALIGNMENT = 3, "Alignment"
    SKILL = 4, "Skill"
    RENOWN = 5, "Renown"
    EXPERIENCE = 6, "Experience"
    QUEST = 7, "Quest"
    RELIC = 8, "Relic"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__, repr(self.__str__()), self.value
        )

    def __str__(self) -> str:
        return self.name
