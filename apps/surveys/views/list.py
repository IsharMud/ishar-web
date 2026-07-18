from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic.list import ListView

from apps.core.views.mixins import NeverCacheMixin

from ..models import Survey, SurveyState


class SurveyListView(LoginRequiredMixin, NeverCacheMixin, ListView):
    """Surveys the account can see; staff additionally see drafts + results."""

    context_object_name = "surveys"
    http_method_names = ("get",)
    model = Survey
    template_name = "surveys.html"

    def get_queryset(self):
        qs = Survey.objects.annotate(num_submissions=Count("submission"))
        if not self.request.user.is_eternal():
            qs = qs.exclude(status=SurveyState.DRAFT)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answered = set(
            self.request.user.survey_submissions.values_list(
                "survey_id", flat=True,
            )
        )
        for survey in context["surveys"]:
            survey.answered = survey.pk in answered
        return context
