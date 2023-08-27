from django.contrib.auth.backends import ModelBackend
from passlib.hash import md5_crypt

from isharweb.models.account import Account


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
        if user:
            if md5_crypt.verify(password, user.password) is True:
                return user
        return None
