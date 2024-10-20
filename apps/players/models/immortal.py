from django.conf import settings

from .base import PlayerBase, PlayerBaseManager


class ImmortalManager(PlayerBaseManager):
    """Filter for players with true_level >= minimum immortal level."""

    def get_queryset(self):
        min_imm = settings.MIN_IMMORTAL_LEVEL
        return super().get_queryset().filter(true_level__gte=min_imm)


class Immortal(PlayerBase):
    """Ishar Immortal (proxy model of PlayerBase, excludes regular players)."""

    objects = ImmortalManager()

    class Meta:
        ordering = (
            "true_level",
            "common__level",
        )
        proxy = True
