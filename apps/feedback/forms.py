from django.core import validators
from django.forms import (
    ModelForm,
    CharField,
    RadioSelect,
    Textarea,
    TextInput,
    TypedChoiceField,
)

from .models.choices import FeedbackSubmissionTypePublic
from .models.submission import FeedbackSubmission


class SubmitFeedbackForm(ModelForm):
    """Form to submit feedback."""

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    submission_type = TypedChoiceField(
        choices=FeedbackSubmissionTypePublic,
        coerce=int,
        # help_text="Type",
        label="",
        widget=RadioSelect(attrs={"aria-label": "Type"}),
    )
    subject = CharField(
        # help_text="Subject / Title",
        label="",
        min_length=1,
        max_length=64,
        validators=(
            validators.MinLengthValidator(limit_value=1),
            validators.MaxLengthValidator(limit_value=64),
        ),
        widget=TextInput(
            attrs={
                "class": "form-control rounded",
                "aria-label": "Subject",
                "placeholder": "Subject / Title",
            }
        ),
    )
    body_text = CharField(
        label="",
        validators=(
            validators.MinLengthValidator(limit_value=1),
            validators.MaxLengthValidator(limit_value=1024),
        ),
        widget=Textarea(
            attrs={
                "class": "form-control rounded",
                "aria-label": "Message",
                "placeholder": "Message",
                "rows": 4,
            }
        ),
    )

    class Meta:
        model = FeedbackSubmission
        fields = ("submission_type", "subject", "body_text")
