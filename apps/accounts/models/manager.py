from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    """Ishar account manager."""

    def create_user(self, email=None, account_name=None, password=None):
        """
        Creates and saves an Account with the given email address,
            account name, and password.
        """
        if not email:
            raise ValueError("E-mail address is required.")

        if not account_name:
            raise ValueError("Account name is required.")

        user = self.model(
            email=self.normalize_email(email),
            account_name=self.normalize_username(account_name)
        )
        user.set_unusable_password()
        if password:
            user.set_password(raw_password=password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, account_name=None, password=None):
        """
        Creates and saves an Account with the given email address,
            account name, and password.
        However, it will not be a "superuser", since no players.
        """
        user = self.create_user(
            email=email,
            account_name=account_name,
            password=password
        )
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, account_name):
        """Natural key of the account username."""
        return self.get(account_name=account_name)
