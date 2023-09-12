from rest_framework import viewsets, permissions

from .models import Race
from .serializers import RaceSerializer


class RacesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows races to be viewed or edited.
    """
    model = Race
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = RaceSerializer
