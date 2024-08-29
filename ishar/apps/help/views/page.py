from re import search

from django.contrib import messages
from django.shortcuts import redirect, reverse
from logging import getLogger

from ..views import HelpView


logger = getLogger(__name__)

class HelpPageView(HelpView):
    """
    Help page view.
    """
    template_name = "help_page.html"

    def dispatch(self, request, *args, **kwargs):

        # Get help topic name from URL.
        help_topic = kwargs.get("help_topic")
        if help_topic is not None:

            # Search the "helptab" file topic names and aliases for string.
            search_results = self.helptab.search(search_name=help_topic)

            # Handle any search results.
            if search_results:

                # Handle single results.
                if len(search_results) == 1:
                    search_result = search_results.pop()

                    # Set exact name matches directly.
                    if help_topic == search_result.name:
                        self.help_topic = search_result
                        return super().dispatch(request, *args, **kwargs)

                    # Redirect single result to proper name of the topic.
                    return redirect(
                        to=reverse(
                            viewname="help_page",
                            args=(search_result.name,)
                        )
                    )

                # Set the help topics to the search results.
                self.help_topics = search_results

            # Tell user if no search results were found.
            else:
                self.status = 404
                messages.error(
                    request=request,
                    message="Sorry, but no such help topic could be found."
                )

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Set HTTP response status code.
        """
        return self.render_to_response(
            context=self.get_context_data(**kwargs),
            status=self.status
        )
