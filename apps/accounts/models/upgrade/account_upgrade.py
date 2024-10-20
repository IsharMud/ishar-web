from django.db import models

from ..account import Account
from .upgrade import AccountUpgrade


class AccountAccountUpgrade(models.Model):
    """Account upgrade relation to an account."""

    account = models.ForeignKey(
        db_column="account_id",
        editable=False,
        to=Account,
        to_field="account_id",
        related_query_name="upgrade",
        related_name="all_upgrades",
        on_delete=models.DO_NOTHING,
        help_text="Account with the specified upgrade.",
        verbose_name="Account",
    )
    upgrade = models.OneToOneField(
        db_column="account_upgrades_id",
        editable=False,
        to=AccountUpgrade,
        to_field="id",
        primary_key=True,
        related_query_name="+",
        on_delete=models.DO_NOTHING,
        help_text="Upgrade which the account has.",
        verbose_name="Upgrade",
    )
    amount = models.PositiveIntegerField(
        db_column="amount",
        help_text="Amount of the account upgrade.",
        verbose_name="Amount",
    )

    # The composite primary key (account_upgrades_id, account_id) found,
    #   that is not supported. The first column is selected.
    class Meta:
        managed = False
        db_table = "accounts_account_upgrades"
        constraints = (
            models.constraints.UniqueConstraint(
                fields=("account", "upgrade"),
                name="one_upgrade_per_account"
            ),
        )
        unique_together = (("account", "upgrade"),)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.amount})"

    def __str__(self) -> str:
        return f"{self.upgrade} @ {self.account}"
