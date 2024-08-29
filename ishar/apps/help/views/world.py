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
        context["areas"] = []
        for topic in self.helptab.search("Area "):
            if topic.is_area is True:
                context["areas"].append(topic)
        return context
