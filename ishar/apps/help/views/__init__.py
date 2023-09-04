from django.views.generic.base import TemplateView

from ..util.helptab import get_help_topics, search_help_topics


HELP_PROPERTIES = [
    'syntax', 'level', 'minimum', 'class', 'topic', 'save', 'stats'
]


class HelpView(TemplateView):
    template_name = "help_page.html.djt"
    extra_context = {
        'help_topic': None,
        'help_topics': get_help_topics(),
        'help_properties': HELP_PROPERTIES
    }


class HelpPageView(HelpView):
    template_name = "help_page.html.djt"

    def __init__(self, help_topic=None):
        self.extra_context['help_topic'] = help_topic
        super().__init__()


class WorldView(HelpView):
    template_name = "world.html.djt"
    extra_context = {"topics": search_help_topics(search='Area ')}
