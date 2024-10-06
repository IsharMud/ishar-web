from django.core import validators
from django.forms import (
    ModelForm, BooleanField, CharField, CheckboxInput, Select, Textarea,
    TextInput, TypedChoiceField
)

from .models.choices import FeedbackSubmissionTypePublic
from .models.submission import FeedbackSubmission


class SubmitFeedbackForm(ModelForm):
    """Form to submit feedback."""

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
#        self.account_id = self.request.user.pk
        super().__init__(*args, **kwargs)

    submission_type = TypedChoiceField(
        choices=FeedbackSubmissionTypePublic,
        coerce=int,
        # help_text="Type",
        label="Type",
        widget=Select(
            attrs={
                "class": "form-control rounded",
                "aria-label": "Type",
            }
        )
    )
    subject = CharField(
        # help_text="Subject / Title",
        label="Subject / Title",
        min_length=1,
        max_length=64,
        validators=(
            validators.MinLengthValidator(limit_value=1),
            validators.MaxLengthValidator(limit_value=64)
        ),
        widget=TextInput(
            attrs={
                "class": "form-control rounded",
                "aria-label": "Subject",
                "placeholder": "Subject / Title",
            }
        )
    )
    body_text = CharField(
        # help_text="Message",
        label="Message",
        validators=(
            validators.MinLengthValidator(limit_value=1),
            validators.MaxLengthValidator(limit_value=1024)
        ),
        widget=Textarea(
            attrs={
                "class": "form-control rounded",
                "aria-label": "Message",
                "placeholder": "Message",
            }
        )
    )
    private = BooleanField(
        # help_text="Private?",
        label="Private?",
        required=False,
        widget=CheckboxInput(
            attrs={
                # "class": "form-control rounded",
                "aria-label": "Private?",
            }
        )
    )

    class Meta:
        model = FeedbackSubmission
        fields = ("submission_type", "subject", "body_text", "private")