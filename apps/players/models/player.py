from django.conf import settings

from .base import PlayerBase, PlayerBaseManager


class PlayerManager(PlayerBaseManager):
    def get_queryset(self):
        # Exclude players with "true_level" >= the minimum immortal level.
        return super().get_queryset().exclude(
            true_level__gte=settings.MIN_IMMORTAL_LEVEL
        )


class Player(PlayerBase):
    """Ishar player (proxy model of PlayerBase, excludes immortals)."""

    objects = PlayerManager()

    class Meta:
        proxy = True
