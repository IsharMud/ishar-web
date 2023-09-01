from rest_framework import viewsets, permissions

from ..models import Player, PlayerClass
from ..serializers import PlayerSerializer, PlayerClassSerializer


class PlayerAPIViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows players to be viewed or edited.
    """
    model = Player
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Player.objects.all()


class PlayerClassAPIViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows classes to be viewed or edited.
    """
    model = PlayerClass
    serializer_class = PlayerClassSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = PlayerClass.objects.all()
