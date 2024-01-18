from django.db import models

from ishar.apps.accounts.models import Account


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
    is_disabled = models.BooleanField(
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
        default_related_name = "upgrade"
        ordering = ("is_disabled", "name")
        verbose_name = "Upgrade"
        verbose_name_plural = "Upgrades"

    def __repr__(self):
        return f"{self.__class__.__name__}: {repr(self.__str__())}"

    def __str__(self) -> str:
        return self.name or self.id


class AccountAccountUpgrade(models.Model):
    """
    Account upgrade relation to an account.
    """
    account = models.ForeignKey(
        primary_key=True,  # Fake it, just so reads work.
        db_column="account_id",
        editable=False,
        to=Account,
        to_field="account_id",
        related_query_name="upgrade",
        related_name="all_upgrades",
        on_delete=models.CASCADE,
        help_text="Account with the specified upgrade.",
        verbose_name="Account"
    )
    upgrade = models.ForeignKey(
        db_column="account_upgrades_id",
        editable=False,
        to=AccountUpgrade,
        to_field="id",
        related_query_name="+",
        on_delete=models.CASCADE,
        help_text="Upgrade which the account has.",
        verbose_name="Upgrade"
    )
    amount = models.PositiveIntegerField(
        db_column="amount",
        help_text="Amount of the account upgrade.",
        verbose_name="Amount"
    )

    # The composite primary key (account_upgrades_id, account_id) found,
    #   that is not supported. The first column is selected.
    class Meta:
        managed = False
        db_table = "accounts_account_upgrades"
        unique_together = (("account", "upgrade"),)

    def __repr__(self):
        return f"{self.__class__.__name__}: {repr(self.__str__())}"

    def __str__(self) -> str:
        return f"{self.upgrade} @ {self.account} : {self.amount}"
