from django.core.management.base import BaseCommand, CommandError

from ishar.apps.accounts.models import Account


class Command(BaseCommand):
    help = "Find players for an account"

    def add_arguments(self, parser):
        parser.add_argument("account", nargs=1, type=str)

    def handle(self, *args, **kwargs):

        try:
            account_name = kwargs["account"][0]
            account = Account.objects.get(account_name=account_name)

        except Account.DoesNotExist:
            raise CommandError('Account "%s" not found!' % kwargs["account"][0])

        self.stdout.write(
            self.style.SUCCESS(
                'Account "%s" has %i players' % (
                    (account.account_name, account.players.count())
                )
            )
        )
        if account.players.count() > 0:
            i = 0
            for player in account.players.all():
                i += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        '\t%i. %s' % (
                            (i, player.name)
                        )
                    )
                )
