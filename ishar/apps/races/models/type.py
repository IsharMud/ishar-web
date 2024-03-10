from django.db.models import IntegerChoices


class AffinityType(IntegerChoices):
    """
    Affinity types.
    """
    VULNERABILITY = 0
    SUSCEPTIBILITY = 1
    RESISTANCE = 2
    IMMUNITY = 3

    def __repr__(self):
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.value
        )

    def __str__(self):
        return self.name.title()
