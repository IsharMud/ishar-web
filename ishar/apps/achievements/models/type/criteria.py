from django.db.models import IntegerChoices


class AchievementCriteriaType(IntegerChoices):
    """Achievement criteria type choices."""
    # Individual means individual character needs to meet criteria.
    INDIVIDUAL = 0
    # Seasonal means your entire account gets aggregated.
    SEASONAL = 1
    # Historic means entire account, and historic stats from previous seasons.
    HISTORIC = 2

    def __repr__(self) -> str:
        return "%s: %s (%s)" % (
            self.__class__.__name__,
            self.__str__(),
            self.value
        )

    def __str__(self) -> str:
        return self.name.title()
