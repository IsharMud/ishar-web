from django.core.management.base import BaseCommand, CommandError

from apps.accounts.models import Account


class Command(BaseCommand):
    """essence command to find essence for account(s)."""

    help = "Find essence for an account."

    def add_arguments(self, parser):
        parser.add_argument("essence", nargs=1, type=str)

    def handle(self, *args, **kwargs):

        account_name = kwargs["essence"][0]
        try:
            account = Account.objects.get(account_name=account_name)
        except Account.DoesNotExist:
            raise CommandError('Account "%s" not found!' % account_name)

        self.stdout.write(
            self.style.SUCCESS(
                '%s\n\t%i essence' % (
                    account.__repr__(),
                    account.current_essence
                )
            )
        )
