from django.views.generic.base import TemplateView
from rest_framework import viewsets, permissions

from .models import Player, PlayerClass
from .models.race import Race
from .models.remort import RemortUpgrade
from .serializers import (
    PlayerSerializer, PlayerClassSerializer, RaceSerializer,
    RemortUpgradeSerializer
)


class PlayerView(TemplateView):
    """
    Player view.
    """
    template_name = "player.html.djt"


class PlayerPageView(PlayerView):
    """
    Player page view.
    """
    def __init__(self, player_name=None):
        player = Player.objects.filter(name__exact=player_name).first()
        self.extra_context["player"] = player
        super.__init__()


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint that allows players to be viewed.
    """
    lookup_field = "name"
    model = Player
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = PlayerSerializer


class PlayerClassViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows classes to be viewed or edited.
    """
    model = PlayerClass
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = PlayerClassSerializer


class RaceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows races to be viewed or edited.
    """
    model = Race
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = RaceSerializer


class RemortUpgradeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows remort upgrades to be viewed or edited.
    """
    model = RemortUpgrade
    serializer_class = RemortUpgradeSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
