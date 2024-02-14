from django.db.models import IntegerChoices


class GameType(IntegerChoices):
    """
    Player character game types.
    """
    CLASSIC = 0
    SURVIVAL = 1
    HARDCORE = 2

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__, self.__str__(), self.value
        )

    def __str__(self) -> str:
        return self.name
