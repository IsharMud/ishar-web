from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.affect_flag import AffectFlag

from .mobile import Mobile


class MobileAffectFlag(models.Model):
    """Ishar mobile affect flag uses affect flag."""

    id = models.AutoField(
        db_column="id",
        blank=False,
        help_text=_(
            "Auto-generated identification number of the mobile affect flag."
        ),
        null=False,
        primary_key=True,
        verbose_name="ID",
    )
    mobile = models.ForeignKey(
        db_column="mob_id",
        to=Mobile,
        to_field="id",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text=_("Mobile affected by the affect flag."),
        verbose_name=_("Mobile"),
    )
    affect_flag = models.ForeignKey(
        db_column="flag_id",
        to=AffectFlag,
        to_field="flag_id",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text=_("Affect flag affecting the mobile."),
        related_name="+",
        verbose_name=_("Affect Flag"),
    )
    value = models.IntegerField(
        help_text=_("Value of the affect flag affecting the mobile."),
        verbose_name=_("Value"),
    )

    class Meta:
        managed = False
        db_table = "mob_affect_flags"
        default_related_name = "affect_flag"
        ordering = ("-id",)
        constraints = (
            models.constraints.UniqueConstraint(
                fields=("mobile", "affect_flag"),
                name="one_affect_per_mobile"
            ),
        )
        unique_together = (("mobile", "affect_flag"),)
        verbose_name = _("Mobile Affect Flag")
        verbose_name_plural = _("Mobile Affect Flags")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return f"{self.affect_flag} @ {self.mobile}"
