"""Shared poll/cancel endpoints for the `web_admin_queue` outbox.

Both staff consoles (events: Eternal+, season: God) enqueue commands and then
poll the same queue, so the read/cancel endpoints live once, here. The floor
is Eternal; season rows are additionally God-guarded on cancel (matching the
enqueue gate — an Eternal must not be able to cancel a God's pending season
command, and the game re-checks privileges on execution anyway).
"""
from django.http import JsonResponse
from django.views.generic.base import View

from ..models.webadmin import WebAdminTask
from ..utils import webadmin
from ..utils.staff import staff_name
from .mixins import EternalRequiredMixin, NeverCacheMixin


def task_json(task: WebAdminTask) -> dict:
    return {
        "id": task.id,
        "command": task.command,
        "status": task.status,
        "result": task.result or "",
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "processed_at": (
            task.processed_at.isoformat() if task.processed_at else None
        ),
    }


def _get_task(request):
    task_id = request.POST.get("task_id", "")
    if not task_id.isdigit():
        return None
    return WebAdminTask.objects.filter(id=int(task_id)).first()


class WebAdminStatusView(EternalRequiredMixin, NeverCacheMixin, View):
    """POST-only status poll for one queued command."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        task = _get_task(request)
        if task is None:
            return JsonResponse({"message": "Unknown task."}, status=404)
        return JsonResponse(task_json(task))


class WebAdminCancelView(EternalRequiredMixin, NeverCacheMixin, View):
    """POST-only cancel of a still-pending command (guarded update — races
    safely against the game's own claim)."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        task = _get_task(request)
        if task is None:
            return JsonResponse({"message": "Unknown task."}, status=404)
        if task.command.startswith("season_") and not request.user.is_god():
            return JsonResponse({"message": "Unknown task."}, status=404)
        cancelled = webadmin.cancel(task.id, staff_name(request.user))
        task.refresh_from_db()
        return JsonResponse({"cancelled": cancelled, **task_json(task)})
