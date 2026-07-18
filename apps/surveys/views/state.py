from django.http import Http404, JsonResponse
from django.utils import timezone
from django.views.generic.base import View

from apps.core.views.mixins import GodRequiredMixin, NeverCacheMixin

from ..models import Survey, SurveyState


class SurveyStateView(GodRequiredMixin, NeverCacheMixin, View):
    """Lifecycle flip from the surveys page: POST { status: draft|open|closed }."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        try:
            survey = Survey.objects.get(slug=kwargs["slug"])
        except Survey.DoesNotExist:
            raise Http404
        status = request.POST.get("status")
        if status not in SurveyState.values:
            return JsonResponse(
                {"ok": False, "message": "Unknown status."}, status=400,
            )
        survey.status = status
        # Reopening past a stale window would stay effectively closed —
        # an explicit Open clears an already-elapsed closes_at.
        if (status == SurveyState.OPEN and survey.closes_at
                and survey.closes_at <= timezone.now()):
            survey.closes_at = None
        survey.save()
        return JsonResponse({
            "ok": True,
            "state_label": survey.state_label,
            "state_pill": survey.state_pill,
        })
