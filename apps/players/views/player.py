from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic.detail import DetailView

from apps.accounts.models import Account
from apps.core.views.mixins import NeverCacheMixin

from ..models.player import Player


class PlayerView(LoginRequiredMixin, NeverCacheMixin, DetailView):
    """Player view."""

    context_object_name = "player"
    model = Player
    slug_field = slug_url_kwarg = query_pk_and_slug = "name"
    template_name = "player.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)

        # A character whose account link is dangling (deleted/orphaned
        #   account row) is treated as private, rather than raising an
        #   uncaught DoesNotExist when its privacy is checked below.
        try:
            is_private = obj.account.is_private
        except Account.DoesNotExist:
            is_private = True

        if is_private:
            # Same 404-for-everyone-else convention as GodRequiredMixin: a
            #   private profile does not disclose its own existence to
            #   anyone below Artisan.
            if not self.request.user.is_artisan():
                raise Http404
            messages.add_message(
                request=self.request,
                level=messages.INFO,
                message="This player has marked their profile private.",
            )
        return obj
