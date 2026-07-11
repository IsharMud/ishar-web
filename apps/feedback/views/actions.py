"""
Staff action endpoint — one POST per `reports` verb, returned as JSON for the
dashboard's AJAX buttons. Eternal is required for the surface (EternalRequiredMixin);
the Gods-only verb (assign_claude) is additionally gated here, mirroring the
in-game `reports claude` level gate.
"""
import json
import logging

from django.core.exceptions import ValidationError
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from apps.core.views.mixins import EternalRequiredMixin, NeverCacheMixin

from .. import services
from ..models import Feedback, FeedbackResolution

log = logging.getLogger(__name__)

# Verbs that require God level, beyond the Eternal gate on the whole surface.
GOD_ONLY_ACTIONS = frozenset({"assign_claude"})


def _run(action, feedback, actor, data):
    """Route a verb to its service call. Raises ValidationError on bad input."""
    if action == "ack":
        return services.acknowledge(feedback, actor)
    if action == "comment":
        return services.comment(feedback, actor, data.get("text", ""))
    if action == "progress":
        return services.set_progress(feedback, actor, data.get("note", ""))
    if action == "resolve":
        return services.close(feedback, actor, FeedbackResolution.FIXED, data.get("note", ""))
    if action == "wontfix":
        return services.close(feedback, actor, FeedbackResolution.WONTFIX, data.get("note", ""))
    if action == "close":
        return services.close(feedback, actor, FeedbackResolution.OTHER, data.get("note", ""))
    if action == "dupe":
        return services.mark_duplicate(feedback, actor, data.get("of_id"))
    if action == "reopen":
        return services.reopen(feedback, actor, data.get("note", ""))
    if action == "bounty":
        return services.bounty(feedback, actor, data.get("note", ""))
    if action == "promote":
        return services.promote(feedback, actor)
    if action == "assign_claude":
        return services.assign_claude(feedback, actor, data.get("instructions", ""))
    raise Http404(f"Unknown feedback action: {action}")


class FeedbackActionView(EternalRequiredMixin, NeverCacheMixin, View):
    """Handle a single staff action against one report."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        action = kwargs.get("action")
        feedback = get_object_or_404(Feedback, pk=kwargs.get("pk"))

        # Gods-only verbs (mirrors the `reports claude` level gate). The whole
        # surface is already Eternal-gated, so a clear JSON 403 is right here.
        if action in GOD_ONLY_ACTIONS and not request.user.is_god():
            return JsonResponse(
                {"ok": False, "message": "Only Gods may assign feedback to Claude."},
                status=403,
            )

        actor = services.staff_name(request.user)

        # Accept both form-encoded and JSON bodies.
        if request.content_type and "application/json" in request.content_type:
            try:
                data = json.loads(request.body or "{}")
            except json.JSONDecodeError:
                return JsonResponse({"ok": False, "message": "Malformed JSON."}, status=400)
        else:
            data = request.POST

        try:
            message = _run(action, feedback, actor, data)
        except ValidationError as exc:
            return JsonResponse(
                {"ok": False, "message": "; ".join(exc.messages)}, status=400
            )
        except Http404:
            raise
        except Exception:  # pragma: no cover - surface a clean error, log detail
            log.exception("feedback: action %s on #%s failed", action, feedback.pk)
            return JsonResponse(
                {"ok": False, "message": "The action could not be completed."},
                status=500,
            )

        feedback.refresh_from_db()
        return JsonResponse({
            "ok": True,
            "message": message,
            "state": feedback.state,
            "status_label": feedback.status_label,
            "status_css": feedback.status_css,
            "acknowledged_by": feedback.acknowledged_by,
            "bountied": feedback.bountied,
            "github_issue_url": feedback.github_issue_url,
        })
