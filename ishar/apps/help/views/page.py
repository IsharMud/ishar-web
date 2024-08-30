from django.contrib import messages
from django.shortcuts import redirect

from ..views import HelpView


class HelpPageView(HelpView):
    """Help page view."""
    template_name = "help_page.html"

    def dispatch(self, request, *args, **kwargs):
        """Handle request for a specific help page. (/help/<topic|search>/)"""

        # Get help topic name from URL.
        help_topic = kwargs.get("help_topic")
        if help_topic is not None:

            # Search the "helptab" file topic names and aliases for string.
            search_results = self.helptab.search(search_name=help_topic)

            # Handle any search results.
            if search_results:

                # Handle single results.
                if len(search_results) == 1:
                    search_result = next(iter(search_results))
                    search_result_topic = search_results[search_result]

                    # Set exact name matches directly.
                    if help_topic == search_result_topic.name:
                        self.help_topic = search_result_topic
                        return super().dispatch(request, *args, **kwargs)

                    # Redirect single result to proper name of the topic.
                    return redirect(to=search_result_topic.get_absolute_url())

                # Set the help topics to the search results.
                self.help_topics = search_results

            # Set response code and tell user if no search results were found.
            else:
                self.status = 404
                messages.error(
                    request=request,
                    message="Sorry, but no such help topic could be found."
                )

        return super().dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        # Return appropriate HTTP response status code.
        response_kwargs["status"] = self.status
        return super().render_to_response(context, **response_kwargs)
