from django.db.models import IntegerChoices


class GameType(IntegerChoices):
    """Player game types."""
    CLASSIC = 0
    SURVIVAL = 1
    HARDCORE = 2

    def __repr__(self) -> str:
        return "%s: %s" % (
            self.__class__.__name__,r
    def __str__(self) -> str:
        return "%s (%i)" % (self.name, self.value)
