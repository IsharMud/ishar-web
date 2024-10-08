from django.db.models import IntegerChoices


class PlayerClass(IntegerChoices):
    """Ishar playable class choices."""

    NEGATIVE_ONE = -1
    WARRIOR = 0
    ROGUE = 1
    CLERIC = 2
    MAGICIAN = 3
    NO_CLASS = 4
    NECROMANCER = 9
    SHAMAN = 11

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.value})"

    def __str__(self) -> str:
        return self.name.title()
