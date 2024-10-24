from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.objects.models.object import Object

from .account import Account


class AccountSoulboundItem(models.Model):
    """Ishar account soulbound item."""

    account_soulbound_id = models.AutoField(
        primary_key=True,
        help_text=_(
            "Primary key for account soulbound item identification number."
        ),
        verbose_name=_("Account Soulbound Item ID")
    )
    item = models.ForeignKey(
        to=Object,
        to_field="vnum",
        on_delete=models.DO_NOTHING,
        db_column="item_id",
        blank=True,
        null=True,
        help_text=_("Item related to account."),
        verbose_name=_("Item"),
    )
    cooldown = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Cool-down for the account soulbound item."),
        verbose_name=_("Cooldown"),
    )
    last_used = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_(
            "Date and time when the account soulbound item was last used."
        ),
        verbose_name=_("Last Used")
    )
    time_gained = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("Time gained for the account soulbound item."),
        verbose_name=_("Time Gained"),
    )
    updated_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_(
            "Date and time when the account soulbound item was last updated."
        ),
        verbose_name=_("Updated At")
    )
    account = models.ForeignKey(
        to=Account,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text=_("Account related to the soulbound item."),
        verbose_name=_("Account"),
    )

    class Meta:
        managed = False
        db_table = "account_soulbound_items"
        default_related_name = "soulbound_item"
        ordering = (
            "item__vnum",
            "account",
        )
        constraints = (
            models.constraints.UniqueConstraint(
                fields=("item", "account",),
                name="soulbound_item_per_account"
            ),
        )
        unique_together = (("item", "account"),)
        verbose_name = "Account Soulbound Item"
        verbose_name_plural = "Account Soulbound Items"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return f"{self.item} @ {self.account}"
