"""
The application form (first submission and revision) and its JSON submit
endpoint. One endpoint covers both: if the account's open application is
awaiting revision, the POST is a resubmit; otherwise it creates a new one.
"""
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import TemplateView, View

from apps.core.views.mixins import NeverCacheMixin

from .. import eligibility, services
from ..models import OPEN_STATUSES, TrialApplication, TrialStatus, TrialTrack


def _open_application(account):
    return (
        TrialApplication.objects.filter(account=account, status__in=OPEN_STATUSES)
        .order_by("-id")
        .first()
    )


class TrialApplyView(LoginRequiredMixin, NeverCacheMixin, TemplateView):
    """The application form — empty, or prefilled for a revision."""

    http_method_names = ("get",)
    template_name = "trial_apply.html"

    def get(self, request, *args, **kwargs):
        application = _open_application(request.user)
        # An application under review isn't editable — show its status instead.
        if application and application.status == TrialStatus.SUBMITTED:
            return redirect("trial_application")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        application = _open_application(user)
        revision_note = None
        if application:
            revision_note = (
                application.comments.filter(
                    is_internal=False, body__startswith="Needs revision:"
                )
                .order_by("-id")
                .values_list("body", flat=True)
                .first()
            )
        context.update({
            "application": application,
            "revision_note": revision_note,
            "eligibility": eligibility.check(user),
            "tracks": TrialTrack.choices,
            "character_names": list(
                user.players.values_list("name", flat=True).order_by("name")
            ),
            "caps": {
                "character": services.CHARACTER_MAX,
                "proposal": services.PROPOSAL_MAX,
                "experience": services.EXPERIENCE_MAX,
            },
        })
        return context


class TrialApplySubmitView(LoginRequiredMixin, NeverCacheMixin, View):
    """JSON submission endpoint — submit or resubmit."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body or b"{}")
        except json.JSONDecodeError:
            return JsonResponse(
                {"ok": False, "message": "Malformed submission."}, status=400
            )
        application = _open_application(request.user)
        try:
            if application and application.status == TrialStatus.NEEDS_REVISION:
                services.resubmit(application, request.user, data)
            else:
                services.submit(request.user, data)
        except ValidationError as exc:
            return JsonResponse(
                {"ok": False, "message": "; ".join(exc.messages)}, status=400
            )
        return JsonResponse({"ok": True, "redirect": reverse("trial_application")})
