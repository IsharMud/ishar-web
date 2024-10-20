"""Ishar MUD server systemctl service utilities."""

from os import getlogin
from subprocess import CalledProcessError, run


def restart_service(name=getlogin()):
    """Run sudo systemctl restart for the MUD service."""
    try:
        command = run(["sudo", "systemctl", "restart", name])
        command.check_returncode()
        return True
    except CalledProcessError:
        return False
