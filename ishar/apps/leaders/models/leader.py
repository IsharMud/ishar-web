from django.conf import settings
from django.db.models import Manager

from ishar.apps.players.models.player import Player


class LeaderManager(Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(
            true_level__gte=settings.MIN_IMMORTAL_LEVEL
        )


class Leader(Player):

    objects = LeaderManager()

    class Meta:
        ordering = (
            "-remorts", "-total_renown", "-quests_completed",
            "-challenges_completed", "deaths"
        )
        proxy = True
