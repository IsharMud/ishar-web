from django.db import models
from django.utils.translation import gettext_lazy as _


class PlayerFlagManager(models.Manager):
    def get_by_natural_key(self, name):
        # Natural key of the player flag name.
        return self.get(name=name)


class PlayerFlag(models.Model):
    """Ishar player flag, used by both mobiles and players."""
    objects = PlayerFlagManager()

    flag_id = models.AutoField(
        db_column="flag_id",
        primary_key=True,
        help_text=_("Auto-generated identification number of the player flag."),
        verbose_name=_("Player Flag ID")
    )
    name = models.CharField(
        blank=False,
        db_column="name",
        max_length=20,
        null=False,
        help_text=_("Name of the player flag."),
        unique=True,
        verbose_name=_("Name")
    )

    class Meta:
        managed = False
        db_table = "player_flags"
        ordering = ("name", "flag_id")
        verbose_name = _("Player/Mobile Flag")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.flag_id})"

    def __str__(self) -> str:
        return self.name

    def natural_key(self) -> str:
        # Natural key of the player flag name.
        return self.name
