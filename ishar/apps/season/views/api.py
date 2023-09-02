from rest_framework import viewsets, permissions

from ..models import Season
from ..serializers import SeasonSerializer


class SeasonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows seasons to be viewed or edited.
    """
    model = Season
    serializer_class = SeasonSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
