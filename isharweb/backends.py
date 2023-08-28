from django.contrib.auth.backends import ModelBackend

from isharweb.models.account import Account
from isharweb.models.quest import Quest


class IsharUserAuthBackend(ModelBackend):
    """
    Ishar authentication backend.
    """
    create_unknown_user = False

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate against MD5Crypt hash from the database for the user.
        """
        user = Account.objects.get(account_name=username)
        if user and user.check_password(raw_password=password):
            return user
        return None

    def get_user(self, user_id=None):
        """
        Get a user by account ID.
        """
        return Account.objects.get(account_id=user_id)
