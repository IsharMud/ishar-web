from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic.detail import DetailView

from apps.accounts.models import Account
from apps.core.views.mixins import NeverCacheMixin

from ..kit import build_kit
from ..models.player import Player


# Standing bars: label, player_stats column.
STANDING_METRICS = (
    ("Renown", "total_renown"),
    ("Hours Played", "total_play_time"),
    ("Quests", "total_quests"),
    ("Challenges", "total_challenges"),
    ("Deaths", "total_deaths"),
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
        stat_fields = [field for _, field in STANDING_METRICS]
        peers = list(
            Player.objects.filter(is_deleted=0).values(
                "id", *[f"statistics__{field}" for field in stat_fields]
            )
        )

        stats = getattr(player, "statistics", None)
        mine = {
            field: getattr(stats, field, 0) or 0 for field in stat_fields
        }

        rows = []
        for label, field in STANDING_METRICS:
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

        # Pace tiles are normalized to this character's own play time and say
        #   so in their labels. "Per hour played" (not per day) keeps the
        #   numbers sane for young characters — a 10-hour character with 3
        #   deaths reads "3.2h / death", not "7.5 deaths / day".
        tiles = []
        hours = mine["total_play_time"] / 3600
        if hours:
            tiles.append({
                "label": "Renown / Hour Played",
                "value": f"{mine['total_renown'] / hours:,.1f}",
                "css": "accent",
            })
            if mine["total_quests"]:
                tiles.append({
                    "label": "Hours Played / Quest",
                    "value": f"{hours / mine['total_quests']:,.1f}h",
                    "css": "info",
                })
            if mine["total_deaths"]:
                tiles.append({
                    "label": "Hours Played / Death",
                    "value": f"{hours / mine['total_deaths']:,.1f}h",
                    "css": "danger",
                })

        return {
            "rows": rows,
            "tiles": tiles,
            "peer_count": len(peers),
            "hours_display": f"{hours:,.0f}h",
        }
