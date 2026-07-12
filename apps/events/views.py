from django.http import JsonResponse
from django.utils.timezone import now
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView

from apps.core.models.webadmin import WebAdminCommand, WebAdminTask
from apps.core.utils import webadmin
from apps.core.utils.staff import staff_name
from apps.core.views.mixins import EternalRequiredMixin, NeverCacheMixin

from .models import EventType, GlobalEvent, WEB_STARTABLE_EVENTS


# Duration units the console accepts, mirroring the in-game `event` command.
DURATION_UNITS = {
    "minutes": 60,
    "hours": 3600,
    "days": 86400,
    "weeks": 604800,
}
# Bounds enforced again game-side (rust web_admin validation).
DURATION_MIN_SECS = 60
DURATION_MAX_SECS = 30 * 86400


class GlobalEventsView(NeverCacheMixin, ListView):
    """Global events view."""

    context_object_name = "global_events"
    model = GlobalEvent
    template_name = "events.html"

    def get_queryset(self):
        current = now()
        return super().get_queryset().filter(
            start_time__lt=current,
            end_time__gt=current
        )


class EventsConsoleView(EternalRequiredMixin, NeverCacheMixin, TemplateView):
    """Staff console: start/extend/end global events. The game executes the
    commands via the web_admin_queue outbox (Eternal+ -> 404 for others)."""

    template_name = "events_console.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current = now()
        active = {
            event.event_type: event
            for event in GlobalEvent.objects.filter(
                start_time__lt=current, end_time__gt=current
            )
        }
        context["event_rows"] = [
            {
                "type": event_type,
                "active": active.get(event_type.value),
                "startable": event_type in WEB_STARTABLE_EVENTS,
            }
            for event_type in EventType
        ]
        context["startable_events"] = WEB_STARTABLE_EVENTS
        context["active_count"] = len(active)
        context["recent_tasks"] = WebAdminTask.objects.filter(
            command__in=(WebAdminCommand.EVENT_START, WebAdminCommand.EVENT_END)
        )[:10]
        return context


class EventActionView(EternalRequiredMixin, NeverCacheMixin, View):
    """POST-only: enqueue an event command. CSRF-protected; inputs are
    allowlisted here and re-validated game-side."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action", "")
        event_type = request.POST.get("event_type", "")
        if not event_type.isdigit():
            return JsonResponse({"message": "Unknown event type."}, status=400)
        event_type = int(event_type)

        if action == "start":
            if event_type not in {e.value for e in WEB_STARTABLE_EVENTS}:
                return JsonResponse(
                    {"message": "That event cannot be started from the web."},
                    status=400,
                )
            amount = request.POST.get("amount", "")
            unit = request.POST.get("unit", "")
            if not amount.isdigit() or int(amount) < 1:
                return JsonResponse(
                    {"message": "Duration must be a positive number."},
                    status=400,
                )
            if unit not in DURATION_UNITS:
                return JsonResponse(
                    {"message": "Unit must be minutes, hours, days or weeks."},
                    status=400,
                )
            duration = int(amount) * DURATION_UNITS[unit]
            if not DURATION_MIN_SECS <= duration <= DURATION_MAX_SECS:
                return JsonResponse(
                    {"message": "Duration must be between 1 minute and 30 days."},
                    status=400,
                )
            task = webadmin.enqueue(
                command=WebAdminCommand.EVENT_START,
                payload={
                    "event_type": event_type,
                    "duration_seconds": duration,
                },
                actor_account=request.user.account_id,
                actor_name=staff_name(request.user),
            )
        elif action == "end":
            if event_type not in {e.value for e in EventType}:
                return JsonResponse({"message": "Unknown event type."}, status=400)
            task = webadmin.enqueue(
                command=WebAdminCommand.EVENT_END,
                payload={"event_type": event_type},
                actor_account=request.user.account_id,
                actor_name=staff_name(request.user),
            )
        else:
            return JsonResponse({"message": "Unknown action."}, status=400)

        return JsonResponse({"queued": True, "task_id": task.id})
