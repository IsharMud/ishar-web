"""God-gated season console.

Season state (`seasons` table) is loaded by the game at boot only and held in
memory, so mutations here never write the table directly — every action
enqueues a `web_admin_queue` command the game executes itself (see
`docs/web_bridge_contracts.md` in ishar-mud). `cycle`/`start` require
password re-auth plus a typed confirmation word: a season cycle deletes every
mortal player.
"""
from datetime import timedelta

from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, now
from django.views.generic.base import TemplateView, View

from apps.core.models.webadmin import WebAdminCommand, WebAdminTask
from apps.core.utils import webadmin
from apps.core.utils.staff import staff_name
from apps.core.views.mixins import GodRequiredMixin, NeverCacheMixin

from ..utils.current import get_current_season


# `seasons.game_state` values — the game's enum game_state_t (constants.h).
GAME_STATES = {
    0: "Normal",
    1: "Season cycle (awaiting start)",
    2: "Maintenance",
    3: "Open beta",
    4: "Closed beta",
}

# The automatic season-end countdown events (game-fired; display only here).
SEASON_END_LADDER = (
    (28, "Rymaras' Echo"),
    (21, "The Comet's Wake"),
    (14, "Twilight of Titans"),
    (7, "Saorin's Reckoning"),
)

EXPIRATION_MAX_DAYS = 366


class SeasonConsoleView(GodRequiredMixin, NeverCacheMixin, TemplateView):
    """Render the season console. God-only (GodRequiredMixin -> 404)."""

    template_name = "season_console.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        season = get_current_season()
        context["season"] = season
        context["game_state_label"] = GAME_STATES.get(
            season.game_state, f"Unknown ({season.game_state})"
        )
        context["game_state_normal"] = season.game_state == 0
        context["game_state_mid_cycle"] = season.game_state == 1
        context["season_end_ladder"] = [
            {
                "days": days,
                "name": name,
                "when": season.expiration_date - timedelta(days=days),
            }
            for days, name in SEASON_END_LADDER
        ]
        context["recent_tasks"] = WebAdminTask.objects.filter(
            command__in=(
                WebAdminCommand.SEASON_SET_EXPIRATION,
                WebAdminCommand.SEASON_SET_AUTO_CYCLE,
                WebAdminCommand.SEASON_CYCLE,
                WebAdminCommand.SEASON_START,
            )
        )[:10]
        return context


class SeasonActionView(GodRequiredMixin, NeverCacheMixin, View):
    """POST-only: enqueue a season command. `set_*` need God + CSRF;
    `cycle`/`start` additionally require password re-auth and a typed
    confirmation word, validated server-side."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action", "")

        if action == "set_expiration":
            raw = request.POST.get("expiration", "")
            when = parse_datetime(raw) if raw else None
            if when is None or not is_aware(when):
                return JsonResponse(
                    {"message": "Expiration must be an ISO datetime with timezone."},
                    status=400,
                )
            current = now()
            if when <= current:
                return JsonResponse(
                    {"message": "Expiration must be in the future."}, status=400
                )
            if when > current + timedelta(days=EXPIRATION_MAX_DAYS):
                return JsonResponse(
                    {"message": "Expiration must be within a year."}, status=400
                )
            command = WebAdminCommand.SEASON_SET_EXPIRATION
            # RFC-3339 with explicit offset, as the game-side validator expects.
            payload = {"expiration_date": when.isoformat()}

        elif action == "set_auto_cycle":
            enabled = request.POST.get("enabled", "")
            if enabled not in ("0", "1"):
                return JsonResponse({"message": "Bad auto-cycle value."}, status=400)
            command = WebAdminCommand.SEASON_SET_AUTO_CYCLE
            payload = {"enabled": enabled == "1"}

        elif action in ("cycle", "start"):
            # Re-auth: password re-entry on the request itself, deploy-style.
            password = request.POST.get("password", "")
            if not password or not request.user.check_password(password):
                return JsonResponse(
                    {"message": "Re-authentication failed."}, status=403
                )
            # Typed confirmation, validated server-side: cycling deletes
            # every mortal player.
            if request.POST.get("confirm", "").strip().lower() != action:
                return JsonResponse(
                    {"message": f'Type "{action}" to confirm.'}, status=400
                )
            command = (
                WebAdminCommand.SEASON_CYCLE
                if action == "cycle"
                else WebAdminCommand.SEASON_START
            )
            payload = {}

        else:
            return JsonResponse({"message": "Unknown action."}, status=400)

        task = webadmin.enqueue(
            command=command,
            payload=payload,
            actor_account=request.user.account_id,
            actor_name=staff_name(request.user),
        )
        return JsonResponse({"queued": True, "task_id": task.id})
