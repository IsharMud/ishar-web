from django.views.generic import TemplateView

from ..utils.current import get_current_season


class CurrentSeasonView(TemplateView):
    template_name = "season.html"
    extra_context = {"season": get_current_season()}
