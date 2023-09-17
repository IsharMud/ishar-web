from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from rest_framework import viewsets, permissions

from .models import Player, RemortUpgrade
from .serializers import PlayerSerializer, RemortUpgradeSerializer


class PlayerView(DetailView):
    """
    Player view.
    """
    context_object_name = "player"
    model = Player
    slug_field = "name"
    slug_url_kwarg = "name"
    query_pk_and_slug = "name"
    template_name = "player.html.djt"


class PlayerSearchView(TemplateView):
    """
    Player search view.
    """
    template_name = "player.html.djt"
    model = Player


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint that allows players to be viewed.
    """
    lookup_field = "name"
    model = Player
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = PlayerSerializer


class RemortUpgradesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows remort upgrades to be viewed or edited.
    """
    model = RemortUpgrade
    serializer_class = RemortUpgradeSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
