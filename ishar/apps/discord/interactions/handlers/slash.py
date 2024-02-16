from .commands import *

from ..exceptions import UnknownCommandException


def slash(interaction_json, request):
    """Handle slash commands."""

    interaction_data = interaction_json.get("data")
    command_name = interaction_data.get("name")

    # "challenges" command to link challenges page.
    if command_name == "challenges":
        return challenges(request=request), False

    # "cycle" command to show when challenges will cycle next.
    if command_name == "cycle":
        return cycle(), False

    # "deadhead" command - player with most deaths.
    if command_name == "deadhead":
        return deadhead(), False

    # "events" command - any active events and when they expire.
    if command_name == "events":
        return events(request=request)

    # "faq" command to link frequently asked questions.
    if command_name == "faq":
        return faq(request=request), False

    # "leaders" command to link leaders page.
    if command_name == "leaders":
        return leaders(request=request), False

    # "mudhelp" command to search MUD help topics.
    if command_name == "mudhelp":
        return mudhelp(request=request, interaction=interaction_data)

    # "spell" command to search MUD help topics for "Spell ".
    if command_name == "spell":
        return mudhelp(
            request=request, interaction=interaction_data, _spell=True
        )

    # "mudtime" command to show server (UTC) time.
    if command_name == "mudtime":
        return mudtime(), False

    # "season" command - shows season number and expiration.
    if command_name == "season":
        return season(request=request), False

    # Raise UnknownCommandException as last resort.
    raise UnknownCommandException
