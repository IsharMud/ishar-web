"""MUD server process utilities."""
from django.db import models
from django.utils.timezone import now

from os import getlogin
from subprocess import CalledProcessError, check_output


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
        help_text="Name of the MUD process.",
        verbose_name="Name"
    )
    last_updated = models.DateTimeField(
        db_column="last_updated",
        default=now,
        help_text=(
            "Last updated date and time of the MUD process in the database."
        ),
        verbose_name="Last Updated"
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


def get_process(name="ishar", user=getlogin()):
    current_process = MUDProcess.objects.filter(
        name__exact=name, user__exact=user
    ).order_by("-last_updated").first()

    try:
        current_pid = check_output(["pgrep", "-u", user, name])
    except CalledProcessError:
        pass
        return None

    if current_pid and current_pid == current_process.process_id:
        return current_process

    MUDProcess.objects.filter(
        name=name,
        user=user,
        last_updated__lt=now()
    ).exclude(
        process_id__exact=current_pid
    ).delete()

    new = MUDProcess(
        process_id=current_pid,
        name=name,
        user=user,
        last_updated=now()
    )
    new.save()
    return new
