"""
Staff action endpoint — one POST per review verb, returned as JSON for the
detail page's buttons. The whole surface is Eternal-gated; the policy names
Eternal, Forger, and God as trial reviewers, so no verb needs a higher gate.
"""
import json
import logging

from django.core.exceptions import ValidationError
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from apps.core.views.mixins import EternalRequiredMixin, NeverCacheMixin

from .. import services
from ..models import TrialApplication

log = logging.getLogger(__name__)


def _run(action, application, actor, data):
    """Route a verb to its service call. Raises ValidationError on bad input."""
    if action == "comment":
        return services.staff_comment(
            application, actor, data.get("text", ""),
            internal=bool(data.get("internal")),
        )
    if action == "needs_revision":
        return services.send_back(application, actor, data.get("note", ""))
    if action == "accept":
        return services.accept(application, actor)
    if action == "reject":
        return services.reject(application, actor, data.get("reason", ""))
    raise Http404(f"Unknown trial action: {action}")


class TrialReviewActionView(EternalRequiredMixin, NeverCacheMixin, View):
    """Handle a single staff action against one application."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        action = kwargs.get("action")
        application = get_object_or_404(TrialApplication, pk=kwargs.get("pk"))
        actor = services.staff_name(request.user)

        # Accept both form-encoded and JSON bodies.
        if request.content_type and "application/json" in request.content_type:
            try:
                data = json.loads(request.body or b"{}")
            except json.JSONDecodeError:
                return JsonResponse(
                    {"ok": False, "message": "Malformed JSON."}, status=400
                )
        else:
            data = request.POST

        try:
            message = _run(action, application, actor, data)
        except ValidationError as exc:
            return JsonResponse(
                {"ok": False, "message": "; ".join(exc.messages)}, status=400
            )
        except Http404:
            raise
        except Exception:  # pragma: no cover - surface a clean error, log detail
            log.exception("trials: action %s on #%s failed", action, application.pk)
            return JsonResponse(
                {"ok": False, "message": "The action could not be completed."},
                status=500,
            )

        application.refresh_from_db()
        return JsonResponse({
            "ok": True,
            "message": message,
            "status": application.status,
            "status_label": application.status_label,
            "status_css": application.status_css,
            "status_pill": application.status_pill,
        })
