from ..views import HelpView


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
