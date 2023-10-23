from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from rest_framework import viewsets, permissions

from ishar.apps.players.models import Player
from ishar.apps.players.models.flag import PlayerFlag, PlayersFlag
from ishar.apps.players.models.upgrade import RemortUpgrade, PlayerRemortUpgrade
from ishar.apps.players.serializers import (
    PlayerSerializer, PlayerFlagSerializer, PlayersFlagSerializer,
    RemortUpgradeSerializer, PlayerRemortUpgradeSerializer
)


class PlayerView(LoginRequiredMixin, DetailView):
    """
    Player view.
    """
    context_object_name = "player"
    model = Player
    slug_field = slug_url_kwarg = query_pk_and_slug = "name"
    template_name = "player.html"


class PlayerSearchView(LoginRequiredMixin, TemplateView):
    """
    Player search view.
    """
    template_name = "player.html"
    model = Player


class PlayerViewSet(viewsets.ModelViewSet):
    """
    Read-only API endpoint that allows players to be viewed.
    """
    lookup_field = "name"
    model = Player
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = PlayerSerializer


class PlayerFlagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows player flags to be viewed or edited.
    """
    model = PlayerFlag
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = PlayerFlagSerializer


class RemortUpgradesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows remort upgrades to be viewed or edited.
    """
    model = RemortUpgrade
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = RemortUpgradeSerializer


class PlayersFlagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows player's flags to be viewed or edited.
    """
    model = PlayersFlag
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = PlayersFlagSerializer


class PlayerRemortUpgradeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows player's remort upgrades to be viewed or edited.
    """
    model = PlayerRemortUpgrade
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = PlayerRemortUpgradeSerializer
