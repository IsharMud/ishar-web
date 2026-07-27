from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic.detail import DetailView

from apps.accounts.models import Account
from apps.core.views.mixins import NeverCacheMixin

from ..kit import build_kit
from ..models.player import Player


# Standing bars: label, player_stats column, per-day rate tile (or None)
#   and the tile's semantic tint.
STANDING_METRICS = (
    ("Renown", "total_renown", "Renown / day", "accent"),
    ("Hours Played", "total_play_time", None, None),
    ("Quests", "total_quests", "Quests / day", "info"),
    ("Challenges", "total_challenges", None, None),
    ("Deaths", "total_deaths", "Deaths / day", "danger"),
)


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
            #   anyone below Artisan — except its own account, who always
            #   sees their own characters.
            user = self.request.user
            if not (user.pk == obj.account_id or user.is_artisan()):
                raise Http404
            messages.add_message(
                request=self.request,
                level=messages.INFO,
                message="This player has marked their profile private.",
            )
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = context["player"]

        # The kit is public (isharmud/ishar-web#176: equipment surfaces like
        #   remort upgrades do); standing/ledger stay the "inspect" layer —
        #   the owning account and Eternal+ staff.
        context["kit"] = build_kit(player)
        user = self.request.user
        can_inspect = user.pk == player.account_id or user.is_eternal()
        context["can_inspect"] = can_inspect
        if can_inspect:
            context["standing"] = self.build_standing(player)
        return context

    @staticmethod
    def build_standing(player) -> dict:
        # Lifetime totals compared against every living mortal character.
        #   player_stats holds snapshot totals only (no history), so the
        #   visuals are comparative, not time-series.
        stat_fields = [field for _, field, _, _ in STANDING_METRICS]
        peers = list(
            Player.objects.filter(is_deleted=0).values(
                "id", *[f"statistics__{field}" for field in stat_fields]
            )
        )

        stats = getattr(player, "statistics", None)
        mine = {
            field: getattr(stats, field, 0) or 0 for field in stat_fields
        }
        days_played = mine["total_play_time"] / 86400

        rows = []
        tiles = []
        for label, field, rate_label, rate_css in STANDING_METRICS:
            values = [peer[f"statistics__{field}"] or 0 for peer in peers]
            value = mine[field]
            top = max(values, default=0)
            if field == "total_play_time":
                display = f"{value / 3600:,.0f}h"
            else:
                display = f"{value:,}"
            rows.append({
                "label": label,
                "display": display,
                # A dead character is outside the living-peer pool, so their
                #   value can exceed the pool's max — clamp the fill.
                "pct": min(100, round(100 * value / top)) if top else 0,
                "rank": 1 + sum(1 for v in values if v > value),
            })
            if rate_label and days_played:
                tiles.append({
                    "label": rate_label,
                    "value": f"{value / days_played:,.1f}",
                    "css": rate_css,
                })

        return {
            "rows": rows,
            "tiles": tiles,
            "peer_count": len(peers),
        }
