from django.db.models import IntegerChoices


class EventType(IntegerChoices):
    """Ishar global event type choices."""
    BONUS_XP = 0
    TEST_SERVER = 1
    CHALLENGE_XP = 2
    CHALLENGE_CYCLE_XP = 3
    CRASH_XP = 4
    WINTER_FEST = 5
    ST_PATRICK = 6
    JULY_FOURTH = 7
    HALLOWS_EVE = 8
    HARVEST_FEST = 9
    MAX_EVENT = 10

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.value
        )

    def __str__(self) -> str:
        return self.name.title()
