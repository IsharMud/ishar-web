"""God-gated engagement track console.

The game holds the live track in memory and validates every change against
its own state (claim receipts, titles, objects), so nothing here writes
`engagement_tracks`: a save enqueues `engagement_set_track` on
`web_admin_queue` and the game applies it (see `docs/web_bridge_contracts.md`
in ishar-mud). Validation here is pre-flight only — see `apps/seasons/tracks.py`.
"""
import json

from django.http import JsonResponse
from django.views.generic.base import TemplateView, View

from apps.core.models.webadmin import WebAdminCommand, WebAdminTask
from apps.core.utils import webadmin
from apps.core.utils.staff import staff_name
from apps.core.views.mixins import GodRequiredMixin, NeverCacheMixin

from .. import tracks
from ..utils.current import get_current_season


class TrackConsoleView(GodRequiredMixin, NeverCacheMixin, TemplateView):
    """Render the engagement track console. God-only (-> 404)."""

    template_name = "track_console.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        season = get_current_season()
        context["season"] = season
        context["track_state"] = tracks.console_state(season)
        context["recent_tasks"] = WebAdminTask.objects.filter(
            command=WebAdminCommand.ENGAGEMENT_SET_TRACK
        )[:8]
        return context


class TrackActionView(GodRequiredMixin, NeverCacheMixin, View):
    """POST-only: queue a track change, or look up an object's name."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action", "")

        if action == "lookup":
            vnum = request.POST.get("vnum", "")
            name = tracks.object_name(int(vnum)) if vnum.isdigit() else None
            if name is None:
                return JsonResponse({"message": "No such object."}, status=404)
            return JsonResponse({"name": name})

        scope = request.POST.get("scope", "")
        if action == "save" and scope in tracks.EDITABLE_SCOPES:
            try:
                raw = json.loads(request.POST.get("milestones", ""))
                milestones = tracks.clean_milestones(raw)
            except json.JSONDecodeError:
                return JsonResponse({"message": "Malformed track."}, status=400)
            except tracks.TrackError as error:
                return JsonResponse({"message": str(error)}, status=400)
        elif action == "revert" and scope in tracks.REVERTIBLE_SCOPES:
            milestones = None
        else:
            return JsonResponse({"message": "Unknown action."}, status=400)

        task = webadmin.enqueue(
            command=WebAdminCommand.ENGAGEMENT_SET_TRACK,
            payload={"scope": scope, "milestones": milestones},
            actor_account=request.user.account_id,
            actor_name=staff_name(request.user),
        )
        return JsonResponse({"queued": True, "task_id": task.id})
