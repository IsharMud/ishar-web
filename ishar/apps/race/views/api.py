from rest_framework import viewsets, permissions

from ..models import Race
from ..serializers import RaceSerializer


class RaceAPIViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows races to be viewed or edited.
    """
    model = Race
    serializer_class = RaceSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Race.objects.all()
