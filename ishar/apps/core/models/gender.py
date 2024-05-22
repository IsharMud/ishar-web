from django.db.models import IntegerChoices


class Gender(IntegerChoices):
    """Ishar gender choices, used by both players and mobiles."""
    MALE = 1
    FEMALE = 2

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.value
        )

    def __str__(self) -> str:
        return self.name.title()
