from django.db.models import IntegerChoices


class GameType(IntegerChoices):
    """Ishar player game types."""
    CLASSIC = 0
    SURVIVAL = 1
    HARDCORE = 2

    def __repr__(self) -> str:
        return "%s: %s" % (
            self.__class__.__name__,
            self.__str__()
        )

    def __str__(self) -> str:
        return "%s (%i)" % (
            self.name.title(),
            self.value
        )
