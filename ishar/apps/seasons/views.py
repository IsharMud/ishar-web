from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions

from .models import Season
from .serializers import SeasonSerializer


class SeasonView(DetailView):
    context_object_name = "publisher"
    model = Season
    template_name = "season.html.djt"

    def get_queryset(self):
        season = get_object_or_404(Season, season_id=self.kwargs["season_id"])
        return season


class SeasonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows seasons to be viewed or edited.
    """
    model = Season
    serializer_class = SeasonSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
