from pprint import pformat

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ngettext

from apps.accounts.models import Account


class Command(BaseCommand):
    """account command to find single account."""

    help = "Find single account."

    def add_arguments(self, parser):
        parser.add_argument("account", nargs=1, type=str)

    def handle(self, *args, **kwargs):

        account_name = kwargs["account"][0]

        try:
            account = Account.objects.get(account_name=account_name)
        except Account.DoesNotExist:
            raise CommandError('Account f"{account_name}" not found!')

        self.stdout.write(self.style.SUCCESS(pformat(vars(account))))

        if account.players:
            num_players = account.players.count()
            phrase = ngettext(
                singular="player",
                plural="players",
                number=num_players
            )
            self.stdout.write(self.style.SUCCESS(f'{num_players} {phrase}'))

            if num_players > 0:

                players = enumerate(account.players.all(), start=1)

                for (num, player) in players:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"\t{num}. {player.__repr__()}"
                        )
                    )

        self.stdout.write(self.style.SUCCESS(account.__repr__()))
