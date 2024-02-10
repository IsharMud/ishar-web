from django.urls import reverse
from django.utils.translation import ngettext

from ishar.apps.help.util import search_help_topics


def mudhelp(request, interaction=None):
    """Link to help topics."""

    # Default message assuming there are no help topics found.
    reply = "Sorry - no help topic(s) could be found."

    # Find help topics, based upon search query.
    search_query = interaction["options"][0]["value"]
    search_results = None
    if search_query:
        search_results = search_help_topics(search=search_query)

    # Proceed if any help topics are found.
    ephemeral = True
    if search_results:
        ephemeral = False
        help_url_prefix = "%s://%s" % (request.scheme, request.get_host())
        help_url_page = search_query
        url_fmt = "<%s%s>"

        num_results = len(search_results)
        if num_results == 1:
            search_result = next(iter(search_results.values()))
            help_url_page = search_result["name"]
            url_fmt = "%s%s"

        help_url = url_fmt % (
            help_url_prefix,
            reverse(viewname="help_page", args=(help_url_page,))
        )

        reply = "%i %s: %s" % (
            num_results,
            ngettext(singular="topic", plural="topics", number=num_results),
            help_url
        )

    # Return the reply.
    return reply, ephemeral
