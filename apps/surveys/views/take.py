import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.views.generic.base import View
from django.views.generic.detail import DetailView

from apps.core.views.mixins import NeverCacheMixin

from ..models import Survey, SurveyState
from ..services import SubmissionError, save_submission


class VisibleSurveyMixin(LoginRequiredMixin):
    """Resolve a survey by slug; drafts exist only for staff (404 otherwise)."""

    def get_survey(self) -> Survey:
        try:
            survey = Survey.objects.prefetch_related(
                "sections", "questions__options", "questions__section",
            ).get(slug=self.kwargs["slug"])
        except Survey.DoesNotExist:
            raise Http404
        if survey.is_draft() and not self.request.user.is_eternal():
            raise Http404
        return survey


class SurveyView(VisibleSurveyMixin, NeverCacheMixin, DetailView):
    """The survey form — or its submitted / closed state."""

    context_object_name = "survey"
    http_method_names = ("get",)
    template_name = "survey.html"

    def get_object(self, queryset=None):
        return self.get_survey()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey = context["survey"]

        # Group questions under their sections in one pass (both prefetched);
        # unsectioned questions render first, numbering runs survey-wide.
        questions = list(survey.questions.all())
        number = 0
        for question in questions:
            number += 1
            question.number = number
        groups = [
            {"section": None, "questions": [q for q in questions if not q.section]}
        ]
        for section in survey.sections.all():
            groups.append({
                "section": section,
                "questions": [q for q in questions if q.section_id == section.pk],
            })
        context.update({
            "groups": [g for g in groups if g["questions"]],
            "question_count": number,
            "answered": survey.submissions.filter(
                account=self.request.user,
            ).exists(),
        })
        return context


class SurveySubmitView(VisibleSurveyMixin, NeverCacheMixin, View):
    """JSON submission endpoint for the survey form."""

    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        survey = self.get_survey()
        try:
            payload = json.loads(request.body or b"{}")
        except json.JSONDecodeError:
            return JsonResponse(
                {"ok": False, "message": "Malformed submission."}, status=400,
            )
        try:
            save_submission(survey, request.user, payload)
        except SubmissionError as error:
            return JsonResponse(
                {"ok": False, "message": error.message, "errors": error.errors},
                status=400,
            )
        return JsonResponse({"ok": True})
