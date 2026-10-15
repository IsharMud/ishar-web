from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.views.generic.list import ListView

from apps.accounts.models import Account
from apps.core.views.mixins import NeverCacheMixin
from apps.players.models import Player

from .context import fated_season_active
from .tension import FATED_CLASS_ID


class TensionLeadersView(LoginRequiredMixin, NeverCacheMixin, ListView):
    """Accounts ranked by the best net Tension at which they completed a
    climb — this season (``season_max_tension``) or lifetime (``max_tension``).
    Ties break on woven essence, then account name. Only a completed climb
    counts: parking at the summit mints nothing."""

    context_object_name = "leaders"
    lifetime = False
    model = Account
    template_name = "tension_leaders.html"

    @property
    def rank_field(self) -> str:
        return "max_tension" if self.lifetime else "season_max_tension"

    def get_queryset(self):
        qs = super().get_queryset().filter(**{f"{self.rank_field}__gt": 0})
        return qs.order_by(
            f"-{self.rank_field}", "-season_woven_essence", "account_name",
        ).prefetch_related(
            # The account's living Fated characters, for the name link.
            Prefetch(
                "players",
                queryset=Player.objects.filter(
                    common__player_class_id=FATED_CLASS_ID, is_deleted=0,
                ).select_related("account", "common"),
                to_attr="fated_players",
            )
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context["lifetime"] = self.lifetime
        context["fated_season"] = fated_season_active()
        return context
