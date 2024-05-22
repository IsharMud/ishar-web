"""Ishar MUD server process model."""
from django.db import models
from django.utils.timesince import timesince
from django.utils.timezone import now
from psutil import Process

from .manager import MUDProcessManager


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
        return "%s: %s [%s]" % (
            self.__class__.name,
            self.__str__(),
            self.user
        )

    def __str__(self):
        return "%s (%i)" % (
            self.name,
            self.process_id
        )

    class Meta:
        managed = True
        db_table = "mud_processes"
        default_related_name = "process"
        ordering = ("-last_updated",)
        verbose_name = "MUD Process"
        verbose_name_plural = "MUD Processes"

    def get_process(self):
        # Get psutil.Process object or the process ID (PID).
        if self.process_id:
            return Process(pid=self.process_id)
        return None

    def kill(self):
        # Send SIGKILL to process.
        if self.process_id:
            process = self.get_process()
            if process:
                try:
                    process.kill()
                    return True
                except:
                    pass
        return False

    def natural_key(self) -> str:
        # Natural key by process name.
        return self.name

    def runtime(self):
        # Human time since process started.
        return timesince(self.created)

    def terminate(self):
        # Send SIGTERM to process.
        if self.process_id:
            process = self.get_process()
            if process:
                try:
                    process.terminate()
                    return True
                except:
                    pass
        return False
