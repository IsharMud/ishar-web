from django.views.generic import TemplateView

from ..utils.current import get_current_season


class CurrentSeasonView(TemplateView):
    template_name = "season.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["season"] = get_current_season()
        return context
