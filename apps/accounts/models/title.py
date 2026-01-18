from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.title import Title

from .account import Account


class AccountTitle(models.Model):
    """Ishar account title."""

    account_titles_id = models.AutoField(
        primary_key=True,
        help_text=_("Primary key identification number for the account title."),
        verbose_name=_("Account Title ID"),
    )
    account = models.ForeignKey(
        blank=True,
        null=True,
        to=Account,
        on_delete=models.DO_NOTHING,
        help_text=_("Account related to a title."),
        verbose_name=_("Account"),
    )
    title = models.ForeignKey(
        blank=True,
        null=True,
        to=Title,
        on_delete=models.DO_NOTHING,
        help_text=_("Title related to an account."),
        verbose_name=_("Title"),
    )

    class Meta:
        managed = False
        db_table = "account_titles"
        ordering = (
            "title",
            "account",
        )
        verbose_name = _("Account Title")
        verbose_name_plural = _("Account Titles")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return f"{self.title} @ {self.account}"
