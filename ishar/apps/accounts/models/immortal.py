from django.db import models

from . import Account


class EternalManager(models.Manager):
    """
    Account manager.
    """
    def get_queryset(self):
        """
        Filter to accounts eternal level and above.
        """
        return super().get_queryset(self).filter(true_level__gte=24)


class ImmortalManager(models.Manager):
    """
    Account manager.
    """
    def get_queryset(self):
        """
        Filter to accounts eternal level and above.
        """
        return super().get_queryset(self).filter(true_level__gte=24)


class Eternal(Account):
    """
    Eternals, proxy model of Account.
    """
    objects = EternalManager()

    class Meta:
        default_related_name = "eternal"
        proxy = True
        verbose_name = "Eternal"

class EternalManager(models.Manager):
    """
    Account manager.
    """
    def get_queryset(self):
        """
        Filter to accounts eternal level and above.
        """
        return super().get_queryset(self).filter(true_level__gte=24)


class Eternal(Account):
    """
    Eternals, proxy model of Account.
    """
    objects = EternalManager()

    class Meta:
        managed = False
        default_related_name = "eternal"
        proxy = True
        verbose_name = "Eternal"
        verbose_name_plural = "Eternals"

    def __repr__(self) -> str:
        return (
                self.__class__.__name__ +
                f" : {repr(self.__str__())} [{self.account_id}]"
        )

    def __str__(self) -> str:
        return f"{self.account_name} ({self.email})"
