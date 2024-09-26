from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.player_flag import PlayerFlag

from .mobile import Mobile


class MobilePlayerFlag(models.Model):
    """Ishar mobile player flag uses player flag."""
    mobile = models.ForeignKey(
        db_column="mob_id",
        to=Mobile,
        to_field="id",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text=_("Mobile affected by the player flag."),
        verbose_name=_("Mobile")
    )
    player_flag = models.ForeignKey(
        db_column="flag_id",
        to=PlayerFlag,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text=_("Player flag associated with the mobile."),
        related_name="+",
        verbose_name=_("Player Flag")
    )
    value = models.IntegerField(
        blank=True,
        null=True,
        help_text=_("Value of the mobile player flag."),
        verbose_name=_("Value")
    )

    class Meta:
        managed = False
        db_table = "mob_player_flags"
        default_related_name = "player_flag"
        ordering = ("-id",)
        unique_together = (("mobile", "player_flag"),)
        verbose_name = _("Mobile Player Flag")
        verbose_name_plural = _("Mobile Player Flags")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return f"{self.flag} @ {self.mobile}"
