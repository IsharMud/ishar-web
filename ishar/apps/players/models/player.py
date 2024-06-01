from django.conf import settings

from .base import PlayerBase, PlayerBaseManager


class PlayerManager(PlayerBaseManager):
    """Exclude players with true_level >= the minimum immortal level."""
    def get_queryset(self):
        min_imm = settings.MIN_IMMORTAL_LEVEL
        return super().get_queryset().exclude(true_level__gte=min_imm)


class Player(PlayerBase):
    """Ishar player (proxy model of PlayerBase, excludes immortals)."""
    objects = PlayerManager()

    class Meta:
        proxy = True
