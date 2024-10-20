from django.db.models import IntegerChoices


class SkillSaveType(IntegerChoices):
    """Skill "req_save" type choices."""

    NEGATIVE_ONE = -1
    FORTITUDE = 0
    REFLEX = 1
    RESILIENCE = 2

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.value})"

    def __str__(self) -> str:
        return self.name.title()
