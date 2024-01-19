"""
isharmud.com authentication backend.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class IsharUserAuthBackend(ModelBackend):
    """Ishar authentication backend."""
    create_unknown_user = False
    model = get_user_model()

    def authenticate(self, request, username=None, password=None, **kwargs):
        """Compare against MD5Crypt hash from the database for the username."""
        try:
            user = self.model.objects.get(account_name=username)
        except self.model.DoesNotExist:
            return None

        if user and user.check_password(raw_password=password):
            return user
        return None

    def get_user(self, user_id=None):
        """Get a user by account ID."""
        return self.model.objects.get(account_id=user_id)
