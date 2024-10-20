from django.db import models
from django.utils.translation import gettext_lazy as _

from .mobile import Mobile


class MobileStat(models.Model):
    """Ishar mobile statistics."""

    mob_stats_id = models.AutoField(
        primary_key=True,
        help_text=_("Auto-generated primary key for mobile statistic ID."),
        verbose_name=_("Mobile Statistics ID"),
    )
    mobile = models.OneToOneField(
        to=Mobile,
        to_field="id",
        db_column="mob_id",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text=_("Mobile associated with the statistic."),
        verbose_name=_("Mobile"),
    )
    num_loaded_all = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Number loaded all time."),
        verbose_name=_("Loaded All"),
    )
    num_loaded_season = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Number loaded for season."),
        verbose_name=_("Loaded Season"),
    )
    num_killed_all = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Number killed by the mobile all time."),
        verbose_name=_("Killed All"),
    )
    num_killed_season = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Number killed by the mobile for the season."),
        verbose_name=_("Killed Season"),
    )
    num_pc_killed_all = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Number of players killed by the mobile all time."),
        verbose_name=_("Players Killed Season"),
    )
    num_pc_killed_season = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Number of players killed by the mobile in the season."),
        verbose_name=_("Players Killed Season"),
    )
    num_encountered_all = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Number encountered for the mobile all time."),
        verbose_name=_("Encountered All"),
    )
    num_encountered_season = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Number encountered for the mobile in the season."),
        verbose_name=_("Encountered Season"),
    )
    num_fled_all = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Number fled for the mobile all time."),
        verbose_name=_("Fled All"),
    )
    num_fled_season = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Number fled for the mobile in the season."),
        verbose_name=_("Fled Season"),
    )

    class Meta:
        managed = False
        db_table = "mob_stats"
        default_related_name = "stat"
        ordering = ("mobile", "mob_stats_id")
        verbose_name = _("Mobile Statistic")
        verbose_name_plural = _("Mobile Statistics")

    def __repr__(self) -> str:
        return f"{self.__str__()} [{self.pk}]"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.mobile}"
