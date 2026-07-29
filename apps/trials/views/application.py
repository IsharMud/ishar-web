"""
The applicant's own view of their application: status, the applicant-facing
timeline, and the reply/withdraw actions. The application is always resolved
from the session account — no ID travels from the client, so there is no
cross-account surface at all.
"""
import json
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import Http404, JsonResponse
from django.views.generic.base import View
from django.views.generic.detail import DetailView

from apps.core.views.mixins import NeverCacheMixin

from .. import services
from ..models import OPEN_STATUSES, TrialApplication

log = logging.getLogger(__name__)


class TrialApplicationView(LoginRequiredMixin, NeverCacheMixin, DetailView):
    """Status page for the account's latest application."""

    context_object_name = "application"
    http_method_names = ("get",)
    template_name = "trial_application.html"

    def get_object(self, queryset=None):
        application = (
            TrialApplication.objects.filter(account=self.request.user)
            .order_by("-id")
            .first()
        )
        if application is None:
            raise Http404
        return application

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["timeline"] = self.object.comments.filter(is_internal=False)
        return context


class TrialApplicantActionView(LoginRequiredMixin, NeverCacheMixin, View):
    """Applicant actions (reply, withdraw) against their own open application."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        action = kwargs.get("action")
        application = (
            TrialApplication.objects.filter(
                account=request.user, status__in=OPEN_STATUSES
            )
            .order_by("-id")
            .first()
        )
        if application is None:
            raise Http404

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
            if action == "reply":
                message = services.applicant_reply(
                    application, request.user, data.get("text", "")
                )
            elif action == "withdraw":
                message = services.withdraw(application, request.user)
            else:
                raise Http404(f"Unknown applicant action: {action}")
        except ValidationError as exc:
            return JsonResponse(
                {"ok": False, "message": "; ".join(exc.messages)}, status=400
            )
        except Http404:
            raise
        except Exception:  # pragma: no cover - surface a clean error, log detail
            log.exception("trials: applicant action %s on #%s failed",
                          action, application.pk)
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
