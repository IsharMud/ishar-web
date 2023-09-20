from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from rest_framework import viewsets, permissions

from .models import Player, PlayerFlag, PlayerRemortUpgrade, RemortUpgrade
from .serializers import PlayerSerializer, PlayerFlagSerializer, \
    RemortUpgradeSerializer


class PlayerView(LoginRequiredMixin, DetailView):
    """
    Player view.
    """
    context_object_name = "player"
    model = Player
    slug_field = slug_url_kwarg = query_pk_and_slug = "name"
    template_name = "player.html.djt"

    def get_context_data(self, **kwargs):
        """
        Include remort upgrades in the context on the player page.
        """
        context = super(PlayerView, self).get_context_data(**kwargs)
        context["remort_upgrades"] = PlayerRemortUpgrade.objects.filter(
            player=self.get_object(),
            value__gt=0
        ).all()
        return context

    def setup(self, request, *args, **kwargs):
        self.extra_context = {
            "remort_upgrades": PlayerRemortUpgrade.objects.filter(
                player=kwargs.get(self.context_object_name),
                value__gt=0
            ).all()
        }
        return super().setup(request, *args, **kwargs)


class PlayerSearchView(LoginRequiredMixin, TemplateView):
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
    serializer_class = RemortUpgradeSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
