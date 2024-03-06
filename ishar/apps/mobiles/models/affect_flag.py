from django.db import models
from django.utils.translation import gettext_lazy as _

from ishar.apps.core.models.affect_flag import AffectFlag

from .mobile import Mobile


class MobileAffectFlag(models.Model):
    """Ishar mobile affect flag."""
    id = models.AutoField(
        db_column="id",
        blank=False,
        help_text=_(
            "Auto-generated identification number of the mobile affect flag."
        ),
        null=False,
        primary_key=True,
        verbose_name="ID"
    )
    mobile = models.ForeignKey(
        db_column="mob_id",
        to=Mobile,
        to_field="id",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text="Mobile affected by the affect flag.",
        verbose_name="Mobile"
    )
    affect_flag = models.ForeignKey(
        db_column="flag_id",
        to=AffectFlag,
        to_field="flag_id",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text="Affect flag affecting the mobile.",
        verbose_name="Affect Flag"
    )
    value = models.IntegerField(
        help_text="Value of the affect flag affecting the mobile.",
        verbose_name="Value"
    )

    class Meta:
        managed = False
        db_table = "mob_affect_flags"
        default_related_name = "affect_flag"
        ordering = ("-id",)
        unique_together = (("mobile", "affect_flag"),)
        verbose_name = "Mobile Affect Flag"
        verbose_name_plural = "Mobile Affect Flags"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self) -> str:
        return "%s @ %s" % (
            self.flag,
            self.mobile
        )
