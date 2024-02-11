from django.db.models import IntegerChoices


class PlayerPosition(IntegerChoices):
    """
    Player positions.
    """
    NEGATIVE_ONE = -1, "Negative One [-1]"
    POSITION_DEAD = 0, "Dead [0]"
    POSITION_DYING = 1, "Dying [1]"
    POSITION_STUNNED = 2, "Stunned [2]"
    POSITION_PARALYZED = 3, "Paralyzed [3]"
    POSITION_SLEEPING = 4, "Sleeping [4]"
    POSITION_HOISTED = 5, "Hoisted [5]"
    POSITION_RESTING = 6, "Resting [6]"
    POSITION_SITTING = 7, "Sitting [7]"
    POSITION_RIDING = 8, "Riding [8]"
    UNUSED_POSN = 9, "Unused [9]"
    POSITION_STANDING = 10, "Standing [10]"
