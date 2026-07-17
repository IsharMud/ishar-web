from django.db import models
from django.utils.translation import gettext_lazy as _

from .room_exit import RoomExit


class RoomExitFlag(models.Model):
    """Ishar per-exit flags (game-owned table; minimal column subset).

    Only the flags the web map renders are modeled; the table also carries
    nopick/wizlock/dropto/nomob/nopath/nohunt/newzone/nonewzone.
    """

    exit = models.OneToOneField(
        to=RoomExit,
        primary_key=True,
        db_column="exit_id",
        on_delete=models.DO_NOTHING,
        related_name="flags",
        help_text=_("Room exit the flags belong to."),
        verbose_name=_("Room Exit ID"),
    )
    flag_door = models.BooleanField(
        default=False,
        help_text=_("Is the exit a door?"),
        verbose_name=_("Door?"),
    )
    flag_closed = models.BooleanField(
        default=False,
        help_text=_("Does the door load closed?"),
        verbose_name=_("Closed?"),
    )
    flag_locked = models.BooleanField(
        default=False,
        help_text=_("Does the door load locked?"),
        verbose_name=_("Locked?"),
    )
    flag_hidden = models.BooleanField(
        default=False,
        help_text=_("Is the exit hidden?"),
        verbose_name=_("Hidden?"),
    )
    flag_climb = models.BooleanField(
        default=False,
        help_text=_("Does the exit require climbing?"),
        verbose_name=_("Climb?"),
    )

    class Meta:
        managed = False
        db_table = "room_exit_flags"
        verbose_name = _("Room Exit Flags")
        verbose_name_plural = _("Room Exit Flags")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return f"Flags @ exit {self.exit_id}"
