from django.db import models
from django.utils.translation import gettext_lazy as _


class RoomManager(models.Manager):
    def get_by_natural_key(self, vnum):
        # Natural key by room vnum.
        return self.get(vnum=vnum)


class Room(models.Model):
    """Ishar room."""

    objects = RoomManager()

    vnum = models.AutoField(
        primary_key=True,
        help_text=_("VNUM of the room (primary ID)."),
        verbose_name=_("Room VNUM"),
    )
    zone_id = models.PositiveIntegerField(
        help_text=_("Zone identification number."),
        # max_length=10,
        null=False,
        verbose_name=_("Zone ID"),
    )
    name = models.CharField(
        default="Unnamed Room",
        help_text=_("Name of the room."),
        max_length=255,
        null=False,
        verbose_name=_("Name")
    )
    description = models.TextField(
        blank=True,
        default=None,
        help_text=_("Description of the room."),
        null=True,
        verbose_name=_("Description"),
    )
    terrain = models.PositiveIntegerField(
        blank=True,
        default=0,
        help_text=_("Terrain of the room."),
        # max_length=3,
        null=True,
        verbose_name=_("Terrain"),
    )
    spec_func = models.CharField(
        blank=True,
        default=None,
        help_text=_("Specific function of the room."),
        max_length=64,
        null=True,
        verbose_name=_("Special Function"),
    )
    is_deleted = models.BooleanField(
        default=False,
        help_text=_("Is the room deleted?"),
        null=False,
        verbose_name=_("Is Deleted?"),
    )
    is_dirty = models.BooleanField(
        default=False,
        help_text=_("Is the room dirty?"),
        null=False,
        verbose_name=_("Is Dirty?"),
    )

    class Meta:
        managed = False
        db_table = "rooms"
        ordering = ("vnum",)
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.name

    def natural_key(self) -> int:
        # Natural key by room vnum.
        return self.vnum
