from django.db.models import Manager
from getpass import getuser


class MUDProcessManager(Manager):

    def get_by_natural_key(self, name):
        """Natural key by process name."""
        return self.get(name=name)

    def get_queryset(self):
        # Limit to the current user account.
        return super().get_queryset().filter(user__exact=getuser())
