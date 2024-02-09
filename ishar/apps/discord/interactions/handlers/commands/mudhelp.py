from django.urls import reverse
from django.utils.translation import ngettext

from ishar.apps.help.util import search_help_topics


def mudhelp(request, interaction=None):
    """Link to help topics."""

    # Default message assuming there are no help topics found.
    reply = "Sorry - no help topic(s) could be found."

    # Find help topics, based upon search query.
    search_query = interaction["options"][0]["value"]
    print("search_query:", search_query)
    search_results = None
    if search_query:
        search_results = search_help_topics(search=search_query)

    # Proceed if any help topics are found.
    ephemeral = True
    if search_results:
        ephemeral = False
        help_url = "<%s://%s%s>" % (
            request.scheme,
            request.get_host(),
            reverse(viewname="help_page", args=(search_query,))
        )
        num_results = len(search_results)
        reply = "%i %s:\n%s\n" % (
            num_results,
            ngettext(singular="topic", plural="topics", number=num_results),
            help_url
        )

    # Return the reply.
    return reply, ephemeral
