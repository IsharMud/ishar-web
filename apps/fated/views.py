from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from apps.accounts.models import Account
from apps.core.views.mixins import NeverCacheMixin
from apps.players.models import Player

from .context import fated_season_active
from .tension import (
    FATED_CLASS_ID, HELP_TOPICS, KNOTS_UNTIED, SUMMIT_REMORTS, Knot, bank,
    burden_table, knot_menu, tenths,
)


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


class FatedView(TemplateView):
    """The Fated season explained from spin to ascension, in the loom's own
    words — for a playerbase meeting permadeath, draws, binds, knots and
    ascension all at once."""

    template_name = "fated.html"
    http_method_names = ("get",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["burden_table"] = burden_table()
        context["bank_floor"] = bank(0)
        context["summit"] = SUMMIT_REMORTS
        context["help_topics"] = HELP_TOPICS
        context["fated_season"] = fated_season_active()
        return context


class KnotsView(TemplateView):
    """The loom's whole menu, family by family, so a life can be planned
    before the thread is spun. A viewer's living Fated character has its
    tied knots marked."""

    template_name = "knots.html"
    http_method_names = ("get",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu = knot_menu()
        tied_mask = 0
        character = None
        user = self.request.user
        if user.is_authenticated:
            character = (
                Player.objects.filter(
                    account_id=user.pk, common__player_class_id=FATED_CLASS_ID,
                    is_deleted=0,
                ).first()
            )
            if character is not None and character.tension_locked != KNOTS_UNTIED:
                tied_mask = character.knots_mask or 0

        families = []
        for knot in menu:
            if not families or families[-1]["key"] != knot.family:
                families.append({"key": knot.family, "knots": []})
            families[-1]["knots"].append(
                Knot(modifier=knot, tied=bool(tied_mask & knot.bit))
            )
        top_weight = sum(f["knots"][-1].weight for f in families)
        context.update({
            "families": families,
            "knot_count": len(menu),
            "top_weight": tenths(top_weight),
            "character": character,
            "tied_any": bool(tied_mask),
            "burden_table": burden_table(),
            "help_topics": HELP_TOPICS,
        })
        return context
