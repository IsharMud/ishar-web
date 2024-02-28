from django.db import models

from ishar.apps.mobs.models.mob_data import MobData
from ishar.apps.players.models.flag import PlayerFlag


class MobPlayerFlags(models.Model):
    id = models.AutoField(
        db_column="id",
        primary_key=True,
        help_text="Auto-generated permanent ID number of the news post.",
        verbose_name="News ID"
    )
    mob = models.ForeignKey(
        db_column="mob_id",
        to=MobData,
        to_field="id",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    flag = models.ForeignKey(
        db_column="flag_id",
        to=PlayerFlag,
        to_field="flag_id",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    value = models.IntegerField(
        blank=True,
        null=True,

    )

    class Meta:
        managed = False
        db_table = "mob_player_flags"
        default_related_name = "mobile_player_flag"
        ordering = ("name",)
        unique_together = (("mob", "flag"),)
        verbose_name = "Mobile Player Flag"
        verbose_name_plural = "Mobile Player Flags"

    def __repr__(self) -> str:
        return "%s: %s [%d]" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self) -> str:
        return "%s (Level %i)" % (
            self.long_name or self.name,
            self.level
        )
