from django.urls import reverse
from django.utils.translation import ngettext

from apps.help.utils.helptab import HelpTab


def mudhelp(request, interaction=None, _spell: bool = False) -> tuple[str, bool]:
    """Search and return links to help topics."""

    # Access and parse "helptab" file.
    helptab = HelpTab()

    # Default message assuming no topics found.
    ephemeral = True
    find_what = "help topic"
    results = {}

    if _spell:
        find_what = "spell"

    # Find help topics, based upon search query.
    reply = f"Sorry no such {find_what} could be found."
    search = interaction["options"][0]["value"]
    if search:
        results = helptab.search(search_name=search)

        # Proceed if any help topic results are found.
        if results:
            ephemeral = False
            num_results = len(results)

            # Link to single result directly.
            reply = ":information_source: ["
            if num_results == 1:
                result = next(iter(results.values()))
                topic_name = result.name
                topic_url = result.get_absolute_url()
                reply += topic_name

            # Link to search for multiple results.
            else:
                topic_url = reverse(
                    viewname="help_page",
                    args=(search,)
                ) + "#topics"
                reply += f"{num_results} results"

            # Append the URL to the Discord reply message.
            reply += f"](<{request.scheme}://{request.get_host()}{topic_url}>)"

    # Return the reply, and boolean whether it should be ephemeral.
    return reply, ephemeral
