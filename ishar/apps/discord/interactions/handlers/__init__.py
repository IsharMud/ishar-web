from .deadhead import deadhead
from .events import events
from .faq import faq
from .season import season
from .mudtime import mudtime

from ..error import error


def handle_command(interaction_data, request):
    """Handle various incoming slash command requests."""
    command_name = interaction_data.get("name")

    # "deadhead" command - player with most deaths.
    if command_name == "deadhead":
        return deadhead()

    # "events" command - any active events and when they expire.
    if command_name == "events":
        return events()

    # "faq" command to link frequently asked questions.
    if command_name == "faq":
        return faq(request)

    # "mudtime" command to show server (UTC) time.
    if command_name == "mudtime":
        return mudtime()

    # "season" command - shows season number and expiration.
    if command_name == "season":
        return season()

    # Last resort is to error with "invalid command".
    return error(message="Invalid command", status=400)
