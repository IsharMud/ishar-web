from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView

from ishar.apps.players.models.player import Player


class PlayerView(LoginRequiredMixin, DetailView):
    """
    Player view.
    """
    context_object_name = "player"
    model = Player
    slug_field = slug_url_kwarg = query_pk_and_slug = "name"
    template_name = "player.html"

    def get_queryset(self):
        return super().get_queryset().filter(account__is_private=False)
