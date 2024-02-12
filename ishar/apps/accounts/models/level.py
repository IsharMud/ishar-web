from django.db.models import IntegerChoices


class ImmortalLevel(IntegerChoices):
    """
    Immortal levels.
    """
    IMM_NONE = 0, "None"
    IMM_IMMORTAL = 1, "Immortal"
    IMM_ARTISAN = 2, "Artisan"
    IMM_ETERNAL = 3, "Eternal"
    IMM_FORGER = 4, "Forger"
    IMM_GOD = 5, "God"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__, repr(self.__str__()), self.value
        )

    def __str__(self) -> str:
        return self.name
