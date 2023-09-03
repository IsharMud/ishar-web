from django.views.generic.base import TemplateView

from ..util.helptab import search_help_topics


class HelpView(TemplateView):
    template_name = "help_page.html.djt"


class HelpPageView(TemplateView):
    template_name = "help_page.html.djt"


class WorldView(TemplateView):
    template_name = "world.html.djt"
    extra_context = {"areas": search_help_topics(search='Area ')}
