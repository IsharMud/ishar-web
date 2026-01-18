from django.db import models
from django.utils.translation import gettext_lazy as _

from .room import Room


class RoomExitManager(models.Manager):
    def get_by_natural_key(self, exit_name):
        # Natural key by room exit name.
        return self.get(exit_name=exit_name)


class RoomExit(models.Model):
    """Ishar room exit."""

    id = models.AutoField(
        blank=False,
        db_column="id",
        help_text=_("Auto-generated identification number of the room exit."),
        null=False,
        primary_key=True,
        verbose_name=_("Room Exit ID"),
    )
    room_vnum = models.ForeignKey(
        to=Room,
        to_field="vnum",
        help_text=_("VNUM of the room."),
        db_column="room_vnum",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        verbose_name=_("Room VNUM"),
        related_name = "+",
    )
    exit_index = models.PositiveIntegerField(
        help_text=_("Index number of the room exit."),
        null=False,
        verbose_name=_("Exit Index"),
    )
    destination_vnum = models.PositiveIntegerField(
        default=None,
        help_text=_("Destination VNUM of the room exit."),
        null=True,
        verbose_name=_("Destination VNUM"),
    )
    exit_name = models.CharField(
        blank=True,
        default="",
        help_text=_("Name of the room exit."),
        max_length=64,
        null=False,
        verbose_name=_("Exit Name"),
    )
    door_name = models.CharField(
        blank=True,
        help_text=_("Name of the room exit door."),
        max_length=128,
        null=True,
        verbose_name=_("Door Name"),
    )
    description = models.TextField(
        blank=True,
        default=None,
        help_text=_("Description of the room exit."),
        null=True,
        verbose_name=_("Description"),
    )
    key_vnum = models.IntegerField(
        blank=True,
        default=None,
        help_text=_("VNUM of the key of the room exit."),
        null=True,
        verbose_name=_("Key VNUM"),
    )
    linked_exit_index = models.IntegerField(
        default=None,
        help_text=_("Index number of the linked room exit."),
        null=True,
        verbose_name=_("Linked Exit Index"),
    )
    size_restriction = models.SmallIntegerField(
        default=None,
        help_text=_("Player height/size restriction of the room exit."),
        null=True,
        verbose_name=_("Size Restriction"),
    )
    skill_modifier = models.IntegerField(
        default=0,
        help_text=_("Skill modifier of the room exit."),
        null=False,
        verbose_name=_("Skill Modifier"),
    )
    trap_type = models.PositiveIntegerField(
        default=0,
        help_text=_("Trap type of the room exit."),
        null=False,
        verbose_name=_("Trap Type"),
    )

    def is_trap(self):
        if self.challenge:
            if self.challenge.count() > 0:
                return True
        return False

    class Meta:
        managed = False
        db_table = "room_exits"
        default_related_name = "room_exit"
        ordering = ("room_vnum", "exit_index", "linked_exit_index", "key_vnum")
        verbose_name = _("Room Exit")
        verbose_name_plural = _("Room Exits")
        unique_together = (("room_vnum", "exit_index"),)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} [{self.id}]"

    def __str__(self) -> str:
        return f"{self.exit_name} ({self.exit_index}) @ {self.room_vnum}"

    def natural_key(self) -> str:
        # Natural key of the room exit name.
        return self.exit_name
