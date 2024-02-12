from django.db.models import IntegerChoices


class SkillType(IntegerChoices):
    """
    Skill types.
    """
    TYPE = 0
    SKILL = 1
    SPELL = 2
    CRAFT = 3

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__, repr(self.__str__()), self.value
        )

    def __str__(self) -> str:
        return self.name
