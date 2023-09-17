from django.views.generic.base import TemplateView

from .util.helptab import get_help_topics, search_help_topics


HELP_PROPERTIES = [
    'syntax', 'level', 'minimum', 'class', 'topic', 'save', 'stats'
]


class HelpView(TemplateView):
    template_name = "help_page.html.djt"
    help_topics = get_help_topics()
    help_topic = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["help_topic"] = self.help_topic
        context["help_topics"] = self.help_topics
        context["help_properties"] = HELP_PROPERTIES
        return context


class HelpPageView(HelpView):
    template_name = "help_page.html.djt"

    def dispatch(self, request, *args, **kwargs):
        help_topic = kwargs.get("help_topic")
        if help_topic and help_topic in self.help_topics:
            self.help_topic = self.help_topics[help_topic]
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["help_topic"] = self.help_topic
        return context


class WorldView(HelpView):
    template_name = "world.html.djt"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        areas = search_help_topics(search='Area ').keys()
        context["areas"] = areas
        print(areas)
        return context
