"""
isharmud.com authentication backend.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import get_object_or_404


class IsharUserAuthBackend(ModelBackend):
    """
    Ishar authentication backend.
    """
    create_unknown_user = False
    model = get_user_model()

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate against MD5Crypt hash from the database for the username.
        """
        user = get_object_or_404(self.model, account_name=username)
        if user and user.check_password(raw_password=password):
            return user
        return None

    def get_user(self, user_id=None):
        """
        Get a user by account ID.
        """
        return self.model.objects.get(account_id=user_id)
