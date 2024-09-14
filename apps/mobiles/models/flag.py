from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.player_flag import PlayerFlag

from .mobile import Mobile


class MobileFlag(models.Model):
    """Ishar mobile flag uses player flag."""
    id = models.AutoField(
        db_column="id",
        primary_key=True,
        help_text=_(
            "Auto-generated permanent identification number of the mobile "
            "player flag."
        ),
        verbose_name=_("Mobile Player Flag ID")
    )
    mobile = models.ForeignKey(
        db_column="mob_id",
        to=Mobile,
        to_field="id",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text=_("Mobile related to the mob player flag."),
        verbose_name=_("Mobile")
    )
    flag = models.ForeignKey(
        db_column="flag_id",
        to=PlayerFlag,
        to_field="flag_id",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text=_("Flag related to the mob player flag."),
        verbose_name=_("Flag")
    )
    value = models.IntegerField(
        blank=True,
        null=True,
        help_text=_("Value of the mob player flag."),
        verbose_name=_("Value")
    )

    class Meta:
        managed = False
        db_table = "mob_player_flags"
        default_related_name = "flag"
        ordering = ("-id",)
        unique_together = (("mobile", "flag"),)
        verbose_name = "Mobile Flag"
        verbose_name_plural = "Mobile Flags"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return f"{self.flag} @ {self.mobile}"
