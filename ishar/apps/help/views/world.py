from django.views.generic.base import TemplateView

from ..util.helptab import search_help_topics


class WorldView(TemplateView):
    template_name = "world.html.djt"
    extra_context = {
        "areas": search_help_topics(search='Area ')
    }


class AreasView(WorldView):
    pass
