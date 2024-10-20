from django.db.models import IntegerChoices


class GameType(IntegerChoices):
    """Ishar player game type choices."""

    CLASSIC = 0
    HARDCORE = 1
    SURVIVAL = 2

    @property
    def title(self):
        return self.name.title()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()}"

    def __str__(self) -> str:
        return f"{self.title} ({self.value})"
