from django.views.generic.base import TemplateView
from rest_framework import viewsets, permissions

from .models import Season
from .serializers import SeasonSerializer


class SeasonView(TemplateView):
    """
    Season view.
    """
    template_name = "season.html.djt"
    current_season = Season.objects.first()
    extra_context = {"season": current_season}


class SeasonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows seasons to be viewed or edited.
    """
    model = Season
    serializer_class = SeasonSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
