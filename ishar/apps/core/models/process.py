"""Ishar MUD server process model."""
from os import getlogin

from django.db import models
from django.utils.timezone import now


class MUDProcessManager(models.Manager):
    """MUD process manager limits to the local user."""
    def get_queryset(self):
        return super().get_queryset().filter(user__exact=getlogin())


class MUDProcess(models.Model):
    """MUD server process."""
    objects = MUDProcessManager()

    process_id = models.PositiveIntegerField(
        db_column="process_id",
        primary_key=True,
        help_text="MUD process ID (PID) on the server.",
        verbose_name="MUD Process ID (PID)"
    )
    name = models.CharField(
        db_column="name",
        default="ishar",
        max_length=32,
        help_text="Name of the MUD process.",
        verbose_name="Name"
    )
    user = models.CharField(
        db_column="user",
        max_length=32,
        help_text="User running the MUD process.",
        verbose_name="User"
    )
    last_updated = models.DateTimeField(
        db_column="last_updated",
        default=now,
        help_text=(
            "Date and time the MUD process was last updated in the database."
        ),
        verbose_name="Last Updated"
    )
    created = models.DateTimeField(
        db_column="created",
        default=None,
        null=True,
        help_text="Date and time the MUD process was created (last restarted).",
        verbose_name="Created"
    )

    def __repr__(self):
        return "%s: %s (%s)" % (
            self.__class__.name,
            self.__str__(),
            self.pid
        )

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = "mud_processes"
        default_related_name = "process"
        ordering = ("-last_updated",)
        verbose_name = "MUD Process"
        verbose_name_plural = "MUD Processes"
