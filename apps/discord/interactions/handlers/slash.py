"""Dispatch incoming Discord slash commands to registered handlers."""

from logging import getLogger

from django.http import HttpRequest

from .commands.base import get_command

# Ensure all command modules are imported so they register themselves.
import apps.discord.interactions.handlers.commands  # noqa: F401


logger = getLogger(__name__)


def slash(interaction_json: dict, request: HttpRequest) -> tuple[str, bool]:
    """Route an incoming slash command to the appropriate handler.

    Returns a ``(message, ephemeral)`` tuple.
    Raises ``LookupError`` for unknown commands.
    """
    interaction_data = interaction_json.get("data", {})
    command_name = interaction_data.get("name", "")

    command_cls = get_command(command_name)
    if command_cls is None:
        raise LookupError(f"Unknown Discord slash command: {command_name!r}")

    return command_cls.execute(
        request=request,
        interaction_data=interaction_data,
    )
