from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView

from .forms import SubmitFeedbackForm
from .models import FeedbackSubmission


class FeedbackView(LoginRequiredMixin, CreateView):
    """Feedback submission form view."""

    form_class = SubmitFeedbackForm
    http_method_names = ("get", "post")
    model = FeedbackSubmission
    success_url = "/"
    template_name = "feedback.html"
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
