from django.db.models import IntegerChoices


class PlayerPosition(IntegerChoices):
    """
    Player positions.
    """
    NEGATIVE_ONE = -1, "Negative One"
    POSITION_DEAD = 0, "Dead"
    POSITION_DYING = 1, "Dying"
    POSITION_STUNNED = 2, "Stunned"
    POSITION_PARALYZED = 3, "Paralyzed"
    POSITION_SLEEPING = 4, "Sleeping"
    POSITION_HOISTED = 5, "Hoisted"
    POSITION_RESTING = 6, "Resting"
    POSITION_SITTING = 7, "Sitting"
    POSITION_RIDING = 8, "Riding"
    UNUSED_POSN = 9, "Unused"
    POSITION_STANDING = 10, "Standing"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__, repr(self.__str__()), self.value
        )

    def __str__(self) -> str:
        return self.name
