from django.db import models
from django.utils.translation import gettext_lazy as _


class Zone(models.Model):
    """Ishar zone (game-owned table; minimal column subset)."""

    id = models.PositiveIntegerField(
        primary_key=True,
        help_text=_("Zone identification number."),
        verbose_name=_("Zone ID"),
    )
    name = models.CharField(
        max_length=100,
        help_text=_("Name of the zone."),
        verbose_name=_("Name"),
    )
    min_level = models.SmallIntegerField(
        default=1,
        help_text=_("Minimum level of the zone."),
        verbose_name=_("Minimum Level"),
    )
    max_level = models.SmallIntegerField(
        default=20,
        help_text=_("Maximum level of the zone."),
        verbose_name=_("Maximum Level"),
    )
    is_live = models.BooleanField(
        default=False,
        help_text=_("Is the zone live?"),
        verbose_name=_("Is Live?"),
    )

    class Meta:
        managed = False
        db_table = "zones"
        ordering = ("id",)
        verbose_name = _("Zone")
        verbose_name_plural = _("Zones")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.name
