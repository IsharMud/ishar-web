from django.views.generic import DetailView, TemplateView
from rest_framework import viewsets, permissions

from ishar.apps.seasons.models import Season
from ishar.apps.seasons.serializers import SeasonSerializer
from ishar.apps.seasons.util import get_current_season


class SeasonView(DetailView):
    context_object_name = "season"
    model = Season
    template_name = "season.html.djt"
    slug_field = "season_id"
    slug_url_kwarg = "season_id"


class CurrentSeasonView(TemplateView):
    template_name = "season.html.djt"
    extra_context = {"season": get_current_season()}


class SeasonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows seasons to be viewed or edited.
    """
    model = Season
    serializer_class = SeasonSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
