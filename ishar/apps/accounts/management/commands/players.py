from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ngettext

from ishar.apps.accounts.models import Account


class Command(BaseCommand):
    """players command to find players for account(s)"""

    # python manage.py players tyler eric
    """
    Account "tyler" (4 players)
            1. Tyler
            2. Perrin
            3. Araris
            4. Dresden
    Account "eric" (1 player)
            1. Enzo
    """
    help = "Find players for an account"

    def add_arguments(self, parser):
        parser.add_argument("accounts", nargs="+", type=str)

    def handle(self, *args, **kwargs):

        for account_name in kwargs["accounts"]:

            try:
                account = Account.objects.get(account_name=account_name)
            except Account.DoesNotExist:
                raise CommandError('Account "%s" not found!' % account_name)

            self.stdout.write(
                self.style.SUCCESS(
                    'Account "%s" (%i %s)' % (
                        account.account_name,
                        account.players.count(),
                        ngettext(
                            singular="player",
                            plural="players",
                            number=account.players.count()
                        )
                    )
                )
            )

            players = enumerate(account.players.all(), start=1)
            for (num, player) in players:
                self.stdout.write(
                    self.style.SUCCESS(
                        "\t%i. %s" % (num, player.name)
                    )
                )
