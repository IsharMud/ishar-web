from ..util import search_help_topics
from ..views import HelpView


class WorldView(HelpView):
    """
    World view.
    """
    template_name = "world.html"

    def get_context_data(self, **kwargs):
        """
        Include "areas" context using the "Area " items from the "helptab" file.
        """
        context = super().get_context_data(**kwargs)
        areas = search_help_topics(search='Area ').keys()
        context["areas"] = areas
        return context
