from django.urls import reverse
from django.utils.translation import ngettext

from ishar.apps.help.util import search_help_topics


def mudhelp(request, interaction=None, _spell=False):
    """Search and return links to help topics."""

    # Default message assuming nothing is found.
    reply = "Sorry - no such help topic could be found."
    if _spell:
        reply = "Sorry - no such spell could be found."

    # Find help topics, based upon search query.
    search_query = interaction["options"][0]["value"]
    search_results = None
    if search_query:
        if _spell:
            search_query = f"Spell {search_query}"
        search_results = search_help_topics(search=search_query)

    # Proceed if any help topics are found.
    ephemeral = True
    if search_results:
        ephemeral = False
        help_url_prefix = "%s://%s" % (request.scheme, request.get_host())
        help_url_page = search_query

        num_results = len(search_results)
        if num_results == 1:
            search_result = next(iter(search_results.values()))
            help_url_page = search_result["name"]

        help_url = "%s%s" % (
            help_url_prefix,
            reverse(viewname="help_page", args=(help_url_page,))
        )

        singular = "topic"
        if _spell:
            singular = "spell"
        plural = singular + "s"

        reply = "%i %s: %s" % (
            num_results,
            ngettext(singular, plural, num_results),
            ngettext(help_url, f"<{help_url}>", num_results),
        )

    # Return the reply.
    return reply, ephemeral
