from .commands import *

from ..exceptions import UnknownCommandException


def slash(interaction_json, request):
    """Handle slash commands."""

    interaction_data = interaction_json.get("data")
    command_name = interaction_data.get("name")

    # "deadhead" command - player with most deaths.
    if command_name == "deadhead":
        return deadhead()

    # "events" command - any active events and when they expire.
    if command_name == "events":
        return events(request=request)

    # "faq" command to link frequently asked questions.
    if command_name == "faq":
        return faq(request=request)

    # "mudhelp" command to link a MUD help topic.
    if command_name == "mudtime":
        return mudhelp(request=request, interaction=interaction_data)

    # "mudtime" command to show server (UTC) time.
    if command_name == "mudtime":
        return mudtime()

    # "season" command - shows season number and expiration.
    if command_name == "season":
        return season(request=request)

    # Raise UnknownCommandException as last resort.
    raise UnknownCommandException
