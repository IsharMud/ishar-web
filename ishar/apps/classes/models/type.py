from django.db.models import IntegerChoices


class PlayerClass(IntegerChoices):
    """
    Player classes.
    """
    NONE = -1, "Negative One"
    WARRIOR = 0, "Warrior"
    ROGUE = 1, "Rogue"
    CLERIC = 2, "Cleric"
    MAGICIAN = 3, "Magician"
    NO_CLASS = 4, "No Class"
    NECROMANCER = 9, "Necromancer"
    SHAMAN = 11, "Shaman"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__, repr(self.__str__()), self.value
        )

    def __str__(self) -> str:
        return self.name
