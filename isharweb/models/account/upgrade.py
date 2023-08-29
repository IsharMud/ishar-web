from django.db import models
from django.contrib import admin

class AccountUpgrade(models.Model):
    """
    Account Upgrade.
    """
    id = models.PositiveIntegerField(
        primary_key=True,
        help_text="Auto-generated permanent ID number of the account upgrade.",
        verbose_name="Account Upgrade ID"
    )
    cost = models.PositiveIntegerField(
        help_text="Cost of the account upgrade.",
        verbose_name="Cost"
    )
    description = models.CharField(
        max_length=400,
        help_text="Description of the account upgrade.",
        verbose_name="Description"
    )
    name = models.CharField(
        unique=True, max_length=80,
        help_text="Name of the account upgrade.",
        verbose_name="Name"
    )
    max_value = models.PositiveIntegerField(
        help_text="Maximum value of the account upgrade.",
        verbose_name="Maximum Value"
    )
    scale = models.IntegerField(
        help_text="Scale of the account upgrade.",
        verbose_name="Scale"
    )
    is_disabled = models.IntegerField(
        choices=[(0, False), (1, True)],
        help_text="Is the account upgrade disabled?",
        verbose_name="Is Disabled?"
    )
    increment = models.IntegerField(
        help_text="Increment of the account upgrade.",
        verbose_name="Increment"
    )
    amount = models.IntegerField(
        help_text="Amount of the account upgrade.",
        verbose_name="Amount"
    )

    class Meta:
        managed = False
        db_table = "account_upgrades"
        ordering = ["is_disabled", "name"]
        verbose_name = "Account Upgrade"
        verbose_name_plural = "Account Upgrades"

    def __repr__(self):
        return f"Account Upgrade: {repr(self.__str__())}"

    def __str__(self) -> str:
        return self.name or self.id

    @admin.display(boolean=True, description="Disabled", ordering="is_disabled")
    def _is_disabled(self) -> bool:
        """
        Boolean whether account upgrade is disabled.
        """
        if self.is_disabled == 1:
            return True
        return False
