from django.views.generic import DetailView, TemplateView

from ishar.apps.seasons.models import Season
from ishar.apps.seasons.util import get_current_season


class SeasonView(DetailView):
    context_object_name = "season"
    model = Season
    template_name = "season.html"
    slug_field = "season_id"
    slug_url_kwarg = "season_id"


class CurrentSeasonView(TemplateView):
    template_name = "season.html"
    extra_context = {"season": get_current_season()}
