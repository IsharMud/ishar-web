from pprint import pformat

from django.core.management.base import BaseCommand, CommandError

from apps.players.models.player import PlayerBase


class Command(BaseCommand):
    """player command to find single player."""

    help = "Find player."

    def add_arguments(self, parser):
        parser.add_argument("player", nargs=1, type=str)

    def handle(self, *args, **kwargs):

        player_name = kwargs["player"][0]

        try:
            player = PlayerBase.objects.get(name=player_name)
        except PlayerBase.DoesNotExist:
            raise CommandError(f'Player ("{player_name}") not found!')

        self.stdout.write(self.style.SUCCESS(pformat(vars(player))))
        self.stdout.write(self.style.SUCCESS(player.account.__repr__()))
        self.stdout.write(self.style.SUCCESS(player.__repr__()))
