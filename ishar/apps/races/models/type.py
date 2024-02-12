from django.db.models import IntegerChoices


class AffinityType(IntegerChoices):
    """
    Affinity types.
    """
    VULNERABILITY = 0, "Vulnerability [0]"
    SUSCEPTIBILITY = 1, "Susceptibility [1]"
    RESISTANCE = 2, "Resistance [2]"
    IMMUNITY = 3, "Immunity [3]"
