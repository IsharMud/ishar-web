from django.views.generic import DetailView

from ..models import Season


class SeasonView(DetailView):
    context_object_name = "season"
    model = Season
    template_name = "season.html"
    slug_field = "season_id"
    slug_url_kwarg = "season_id"
