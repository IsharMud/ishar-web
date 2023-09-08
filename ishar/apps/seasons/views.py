from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions

from .models import Season
from .serializers import SeasonSerializer


class SeasonView(DetailView):
    context_object_name = "publisher"
    model = Season
    template_name = "season.html.djt"
    slug_field = "season_id"
    slug_url_kwarg = "season_id"


class SeasonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows seasons to be viewed or edited.
    """
    model = Season
    serializer_class = SeasonSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
