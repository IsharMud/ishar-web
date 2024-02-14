from django.db.models import IntegerChoices


class QuestStepType(IntegerChoices):
    """
    Quest step types.
    """
    OBJECT = 0
    KILL = 1
    ROOM = 2

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__, self.__str__(), self.value
        )

    def __str__(self) -> str:
        return self.name
