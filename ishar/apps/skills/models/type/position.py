from django.db.models import IntegerChoices


class PlayerPosition(IntegerChoices):
    """
    Ishar player position.
    """
    NEGATIVE_ONE = -1
    DEAD = 0
    DYING = 1
    STUNNED = 2
    PARALYZED = 3
    SLEEPING = 4
    HOISTED = 5
    RESTING = 6
    SITTING = 7
    RIDING = 8
    UNUSED = 9
    STANDING = 10

    def __repr__(self) -> str:
        return "%s: %s (%s)" % (
            self.__class__.__name__,
            self.__str__(),
            self.value
        )

    def __str__(self) -> str:
        return self.name.title()
