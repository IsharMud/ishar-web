from django.db import models

from ishar.apps.players.models.flag import PlayerFlag

from .mobile import Mobile


class MobileFlag(models.Model):
    """Mobile player flag."""
    id = models.AutoField(
        db_column="id",
        primary_key=True,
        help_text="Auto-generated permanent ID number of the mob player flag.",
        verbose_name="Mob Player Flag ID"
    )
    mobile = models.ForeignKey(
        db_column="mob_id",
        to=Mobile,
        to_field="id",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text="Mobile related to the mob player flag.",
        verbose_name="Mobile"
    )
    flag = models.ForeignKey(
        db_column="flag_id",
        to=PlayerFlag,
        to_field="flag_id",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text="Flag related to the mob player flag.",
        verbose_name="Flag"
    )
    value = models.IntegerField(
        blank=True,
        null=True,
        help_text="Value of the mob player flag.",
        verbose_name="Value"
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
