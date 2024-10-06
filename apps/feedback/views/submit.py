from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.edit import CreateView

from apps.core.views.mixins import NeverCacheMixin

from ..forms import SubmitFeedbackForm
from ..models.submission import FeedbackSubmission


class SubmitFeedbackView(LoginRequiredMixin, NeverCacheMixin, CreateView):
    """Feedback submission creation form view."""

    form_class = SubmitFeedbackForm
    http_method_names = ("get", "post")
    model = FeedbackSubmission
    success_url = "/feedback/#feedback"
    template_name = "submit.html"
    user = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        self.user = self.request.user
        return kwargs

    def form_valid(self, form):
        if (
            form.cleaned_data and
            form.cleaned_data.get("submission_type") and
            form.cleaned_data.get("subject") and
            form.cleaned_data.get("body_text")
        ):
            form.instance.account = self.user
            messages.success(
                request=self.request,
                message="Thank you! Your feedback has been submitted."
            )
        return super().form_valid(form)
