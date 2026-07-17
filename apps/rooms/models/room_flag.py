from django.db import models
from django.utils.translation import gettext_lazy as _

from .room import Room


class RoomFlag(models.Model):
    """Ishar per-room flags (game-owned table; minimal column subset).

    Only the flags the web map renders are modeled; the table carries ~27
    more booleans the site has no use for yet.
    """

    room = models.OneToOneField(
        to=Room,
        primary_key=True,
        db_column="room_vnum",
        on_delete=models.DO_NOTHING,
        related_name="flags",
        help_text=_("Room the flags belong to."),
        verbose_name=_("Room VNUM"),
    )
    flag_death = models.BooleanField(
        default=False,
        help_text=_("Is the room a death trap?"),
        verbose_name=_("Death?"),
    )
    flag_peaceful = models.BooleanField(
        default=False,
        help_text=_("Is the room peaceful (no combat)?"),
        verbose_name=_("Peaceful?"),
    )

    class Meta:
        managed = False
        db_table = "room_flags"
        verbose_name = _("Room Flags")
        verbose_name_plural = _("Room Flags")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return f"Flags @ {self.room_id}"
