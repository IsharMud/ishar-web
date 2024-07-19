from django.db.models import IntegerChoices


class SkillCooldownType(IntegerChoices):
    """Skill cooldown type choices."""
    ZERO = 0
    NEGATIVE_ONE = -1
    SOMETHING = 1

    def __repr__(self) -> str:
        return "%s: %s (%s)" % (
            self.__class__.__name__,
            self.__str__(),
            self.value
        )

    def __str__(self) -> str:
        return self.name.title()
