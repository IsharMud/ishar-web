from django.db.models import IntegerChoices


class ImmortalLevel(IntegerChoices):
    """Immortal level choices."""
    NONE = 0
    IMMORTAL = 1
    ARTISAN = 2
    ETERNAL = 3
    FORGER = 4
    GOD = 5

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.value
        )

    def __str__(self):
        return self.name.title()
