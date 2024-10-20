from django.db import models

from apps.objects.models.object import Object


class AccountUpgradeManager(models.Manager):
    def get_by_natural_key(self, name):
        # Natural key by account upgrade name.
        return self.get(name=name)


class AccountUpgrade(models.Model):
    """Ishar account upgrade, purchased with essence."""

    objects = AccountUpgradeManager()

    id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated permanent ID number of the account upgrade.",
        verbose_name="Account Upgrade ID",
    )
    cost = models.PositiveIntegerField(
        help_text="Cost of the account upgrade.",
        verbose_name="Cost",
    )
    description = models.CharField(
        max_length=400,
        help_text="Description of the account upgrade.",
        verbose_name="Description",
    )
    name = models.CharField(
        unique=True,
        max_length=80,
        help_text="Name of the account upgrade.",
        verbose_name="Name",
    )
    max_value = models.PositiveIntegerField(
        help_text="Maximum value of the account upgrade.",
        verbose_name="Maximum Value",
    )
    scale = models.IntegerField(
        help_text="Scale of the account upgrade.",
        verbose_name="Scale",
    )
    is_disabled = models.BooleanField(
        help_text="Is the account upgrade disabled?",
        verbose_name="Is Disabled?",
    )
    increment = models.IntegerField(
        help_text="Increment of the account upgrade.",
        verbose_name="Increment",
    )
    amount = models.IntegerField(
        help_text="Amount of the account upgrade.",
        verbose_name="Amount",
    )
    grants_memory = models.ForeignKey(
        to=Object,
        to_field="vnum",
        on_delete=models.DO_NOTHING,
        db_column="grants_memory",
        blank=True,
        null=True,
        help_text="Grants memory of the account upgrade.",
        verbose_name="Grants Memory",
    )

    class Meta:
        managed = False
        db_table = "account_upgrades"
        default_related_name = "upgrade"
        ordering = ("is_disabled", "name")
        verbose_name = "Upgrade"
        verbose_name_plural = "Upgrades"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.description or self.name

    def natural_key(self) -> str:
        # Natural key by account upgrade name.
        return self.name
