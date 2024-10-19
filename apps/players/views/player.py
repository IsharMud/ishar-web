from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView

from apps.core.views.mixins import NeverCacheMixin

from ..models.player import Player


class PlayerView(LoginRequiredMixin, NeverCacheMixin, DetailView):
    """Player view."""

    context_object_name = "player"
    model = Player
    slug_field = slug_url_kwarg = query_pk_and_slug = "name"
    template_name = "player.html"

    def dispatch(self, request, *args, **kwargs):
    # Tell immortals if they are viewing a private profile.
        if request.user:
            if request.user.is_authenticated and request.user.is_immortal():
                obj = self.get_object()
                if obj.account.is_private:
                    messages.add_message(
                        request=request,
                        level=messages.INFO,
                        message="This player has marked their profile private."
                    )
        return super().dispatch(request, *args, **kwargs)
