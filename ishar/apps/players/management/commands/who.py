
from django.core.management.base import BaseCommand, CommandError
from django.db.models import F

from ishar.apps.players.models.player import Player


class Command(BaseCommand):
    """who command to find players online."""

    help = "Find online players."

    def handle(self, *args, **kwargs):

        players = Player.objects.filter(logon__gte=F("logout"))

        if players and players.count() > 0:
            for player in players:
                self.stdout.write(self.style.SUCCESS(player.__repr__()))

        else:
            self.stdout.write(self.style.WARNING("No online players found."))
