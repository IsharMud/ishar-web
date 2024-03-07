"""Ishar MUD server process utilities."""
from datetime import datetime
from os import getlogin
from subprocess import CalledProcessError, check_output

from django.utils.timezone import now
from psutil import Process

from ..models.process import MUDProcess


def get_process(name="ishar", user=getlogin()):
    """Get Ishar MUD process information for appropriate environment."""

    # Find existing process in the database.
    current_process = MUDProcess.objects.filter(
        name__exact=name,
        user__exact=user
    ).order_by("-last_updated").first()

    # Find the actual running Ishar process ID (PID).
    try:
        current_pid = check_output(["pgrep", "-u", user, name])
        current_pid = int(current_pid.decode().strip())
    except (CalledProcessError, ValueError):
        pass
        return None

    # Use the existing database record, if it is correct.
    if current_process and current_pid:
        if current_process.process_id:
            if current_pid == current_process.process_id:
                return current_process

    # Otherwise, delete any existing database records for this environment.
    MUDProcess.objects.filter(
        name=name,
        user=user,
        last_updated__lt=now()
    ).exclude(
        process_id__exact=current_pid
    ).delete()

    # Save and return the latest correct process ID information.
    new = MUDProcess(
        process_id=current_pid,
        name=name,
        user=user,
        last_updated=now(),
        created=datetime.fromtimestamp(Process(pid=current_pid).create_time())
    )
    new.save()
    return new
