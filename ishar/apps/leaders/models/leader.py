from django.conf import settings
from django.db.models import Manager

from ishar.apps.players.models.player import Player


class LeaderManager(Manager):
    """Ishar leader database manager."""

    def get_by_natural_key(self, name):
        # Natural key is player's name.
        return self.get(name=name)

    def get_queryset(self):
        # Exclude immortal characters.
        return super().get_queryset().exclude(
            true_level__gte=settings.MIN_IMMORTAL_LEVEL
        )


class Leader(Player):
    """Ishar leader."""
    objects = LeaderManager()

    class Meta:
        # Re-order proxy model of Player.
        ordering = (
            "-remorts", "-total_renown", "-challenges_completed", "deaths"
        )
        proxy = True

    def natural_key(self):
        # Natural key is player's name.
        return self.name
