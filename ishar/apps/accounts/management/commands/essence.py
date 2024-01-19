from django.core.management.base import BaseCommand, CommandError

from ishar.apps.accounts.models import Account


class Command(BaseCommand):
    """essence command to find essence for account(s)"""

    # python manage.py essence tyler eric
    """
    Account "tyler": 50 essence
    Account "eric": 7 essence
    """
    help = "Check the amount of essence for an account"

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
                    'Account "%s": %i essence' % (
                        account.account_name, account.current_essence
                    )
                )
            )
