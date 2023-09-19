from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.base import TemplateView

from .util.helptab import get_help_topics, search_help_topics


HELP_PROPERTIES = (
    "syntax", "level", "minimum", "class", "component", "topic", "save", "stats"
)


class HelpView(TemplateView):
    template_name = "help_page.html.djt"
    help_topics = get_help_topics()
    help_topic = None
    status = 200

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["help_topic"] = self.help_topic
        context["help_topics"] = self.help_topics
        context["help_properties"] = HELP_PROPERTIES
        return context


class HelpPageView(HelpView):
    template_name = "help_page.html.djt"

    def dispatch(self, request, *args, **kwargs):

        # Get help topic name from URL, and continue if it is not None
        help_topic = kwargs.get("help_topic")
        if help_topic is not None:

            # Set the help topic for the context if a name matched exactly.
            if help_topic in self.help_topics:
                self.help_topic = self.help_topics[help_topic]

            # Non-exact matches are more work.
            if not self.help_topic:

                # Redirect to the main help topic, if an alias matched.
                for (topic_name, topic_value) in self.help_topics.items():
                    aliases = topic_value.get("aliases")
                    if aliases and help_topic in aliases:
                        return redirect(to="help_page", help_topic=topic_name)

                # Search for the topic name, if no aliases matched.
                search_topics = search_help_topics(search=help_topic)
                if search_topics:

                    # Redirect to match, if single search result.
                    if len(search_topics) == 1:
                        return redirect(
                            to="help_page",
                            help_topic=search_topics.popitem()[0]
                        )

                    self.help_topics = search_topics

                # 404 with error message, if no search results.
                if not search_topics:
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


class WorldView(HelpView):
    """
    World view.
    """
    template_name = "world.html.djt"

    def get_context_data(self, **kwargs):
        """
        Include "areas" context using the "Area " items from the "helptab" file.
        """
        context = super().get_context_data(**kwargs)
        areas = search_help_topics(search='Area ').keys()
        context["areas"] = areas
        return context
