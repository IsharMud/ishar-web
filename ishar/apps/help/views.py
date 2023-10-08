from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.base import TemplateView


from ishar.apps.help.forms import HelpSearchForm
from ishar.apps.help.util import get_help_topics, search_help_topics


HELP_PROPERTIES = (
    "syntax", "level", "minimum", "class", "component", "topic", "save", "stats"
)


class HelpView(TemplateView):
    template_name = "help_page.html.djt"
    help_topics = get_help_topics()
    help_topic = None
    http_method_names = ("get", "post")
    search_form = HelpSearchForm()
    status = 200

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["help_properties"] = HELP_PROPERTIES
        context["help_search_form"] = self.search_form
        context["help_topic"] = self.help_topic
        context["help_topics"] = self.help_topics
        return context

    @staticmethod
    def post(request, *args, **kwargs):
        print(request.POST.get("search_topic"))
        return redirect(
            to="help_page",
            help_topic=request.POST.get("search_topic")
        )


class HelpPageView(HelpView):
    template_name = "help_page.html.djt"

    def dispatch(self, request, *args, **kwargs):

        # Get help topic name from URL.
        help_topic = kwargs.get("help_topic")
        if help_topic is not None:
            if help_topic in self.help_topics:
                self.help_topic = self.help_topics[help_topic]
                return super().dispatch(request, *args, **kwargs)

            search_topics = search_help_topics(self.help_topics, help_topic)
            if not search_topics:
                messages.error(
                    request=request,
                    message="Sorry, but no such help topic was found."
                )
                self.status = 404

            if search_topics:
                if len(search_topics) == 1:
                    found_topic = next(iter(search_topics.values()))
                    return redirect(
                        to="help_page", help_topic=found_topic["name"]
                    )
                self.help_topics = search_topics

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
