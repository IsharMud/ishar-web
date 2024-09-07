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
            raise CommandError('Account "%s" not found!' % account_name)

        self.stdout.write(self.style.SUCCESS(pformat(vars(account))))

        if account.players:

            self.stdout.write(
                self.style.SUCCESS(
                    '%i %s' % (
                        account.players.count(),
                        ngettext(
                            singular="player",
                            plural="players",
                            number=account.players.count()
                        )
                    )
                )
            )

            if account.players.count() > 0:

                players = enumerate(account.players.all(), start=1)

                for (num, player) in players:
                    self.stdout.write(
                        self.style.SUCCESS(
                            "\t%i. %s" % (num, player.__repr__())
                        )
                    )

        self.stdout.write(self.style.SUCCESS(account.__repr__()))
