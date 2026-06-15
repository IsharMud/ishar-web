"""Ishar MUD server systemctl service utilities."""

from getpass import getuser
from subprocess import CalledProcessError, run


def restart_service(name=None):
    """Run sudo systemctl restart for the MUD service."""
    if name is None:
        name = getuser()
    try:
        command = run(["sudo", "systemctl", "restart", name])
        command.check_returncode()
        return True
    except CalledProcessError:
        return False
