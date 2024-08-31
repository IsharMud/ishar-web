from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.base import TemplateView

from .forms import HelpSearchForm
from .utils.helptab import HelpTab


class HelpView(TemplateView):
    """Help view."""
    template_name = "help_page.html"
    helptab = HelpTab()
    help_topic = None
    help_topics = {}
    http_method_names = ("get", "post")
    search_form = HelpSearchForm()
    status = 200

    def setup(self, request, *args, **kwargs):
        # Gather help topics from "helptab" file.
        self.help_topics = self.helptab.help_topics
        super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """Handle request for a specific help page. (/help/<topic|search>/)"""

        # Get help topic name from URL.
        help_topic = kwargs.get("help_topic")
        if help_topic is not None:

            # Search the "helptab" file topic names and aliases for string.
            search_results = self.helptab.search(search_name=help_topic)

            # Handle any search results.
            if search_results:

                # Handle single result.
                if len(search_results) == 1:
                    search_result = next(iter(search_results.values()))

                    # Set exact name matches directly.
                    if help_topic == search_result.name:
                        self.help_topic = search_result
                        return super().dispatch(request, *args, **kwargs)

                    # Redirect single result to proper name of the topic.
                    return redirect(to=search_result.get_absolute_url())

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


    def get_context_data(self, **kwargs):
        # Include form, all help topics, and any specific help topic chosen.
        context = super().get_context_data(**kwargs)
        context["help_search_form"] = self.search_form
        context["help_topics"] = self.help_topics
        context["help_topic"] = self.help_topic
        return context

    def render_to_response(self, context, **response_kwargs):
        # Return appropriate HTTP response status code.
        response_kwargs["status"] = self.status
        return super().render_to_response(context, **response_kwargs)

    def post(self, request, *args, **kwargs):
        # Redirect POST requests to HTTP GET search for the help topic string.
        return redirect(
            to="help_page",
            help_topic=request.POST.get("search_topic")
        )


class WorldView(HelpView):
    """World view."""
    template_name = "world.html"

    def get_context_data(self, **kwargs):
        # Include sorted "areas" context of "Area " topics in "helptab" file.
        context = super().get_context_data(**kwargs)
        context["areas"] = []
        for topic_name, topic in self.helptab.search("Area ").items():
            if topic.is_area is True:
                context["areas"].append(topic)
        context["areas"] = sorted(context["areas"])
        return context
