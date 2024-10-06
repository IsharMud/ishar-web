from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Account

from .choices import FeedbackSubmissionType


class FeedbackSubmissionManager(models.Manager):
    def get_by_natural_key(self, submission_id):
        # Natural key has to be the ID.
        return self.get(submission_id=submission_id)


class FeedbackSubmission(models.Model):
    """Ishar website feedback submission."""

    objects = FeedbackSubmissionManager()

    submission_id = models.AutoField(
        blank=False,
        db_column="submission_id",
        help_text=_(
            "Auto-generated permanent ID number of the feedback submission."
        ),
        null=False,
        primary_key=True,
        verbose_name=_("Submission ID")
    )
    submission_type = models.IntegerField(
        blank=False,
        choices=FeedbackSubmissionType,
        db_column="submission_type",
        default=FeedbackSubmissionType.OTHER,
        null=False,
        help_text=_("Type of the feedback submission."),
        verbose_name=_("Type")
    )
    subject = models.CharField(
        max_length=64,
        blank=False,
        db_column="subject",
        help_text=_("Subject of the feedback submission."),
        null=False,
        validators=(
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=64)
        ),
        verbose_name=_("Subject")
    )
    body_text = models.TextField(
        blank=False,
        db_column="body_text",
        help_text=_("Body text of the feedback submission."),
        null=False,
        verbose_name=_("Message")
    )
    private = models.BooleanField(
        db_column="private",
        default=False,
        help_text=_("Should the feedback submission be private?"),
        verbose_name=_("Private?")
    )
    account = models.ForeignKey(
        db_column="account_id",
        blank=False,
        help_text=_("Account that submitted the feedback."),
        null=False,
        on_delete=models.DO_NOTHING,
        to=Account,
        to_field="account_id",
        verbose_name=_("Account")
    )
    submitted = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        db_column="submitted",
        help_text=_("Date and time when the feedback was submitted."),
        null=False,
        verbose_name=_("Submitted")
    )

    class Meta:
        managed = True
        db_table = "feedback"
        default_related_name = "submission"
        get_latest_by = ("submitted",)
        ordering = ("-submitted",)
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} [{self.pk}]"

    def __str__(self) -> str:
        return f"{self.subject} ({self.get_submission_type_display()})"

    def natural_key(self) -> int:
        # Natural key has to be the ID.
        return self.submission_id

    def is_complete(self) -> bool:
        if self.submission_type == FeedbackSubmissionType.COMPLETE:
            return True
        return False

    def is_private(self) -> bool:
        return self.private

    def mark_complete(self) -> bool:
        try:
            self.submission_type = FeedbackSubmissionType.COMPLETE
            self.save()
            return True
        except:
            raise

    def get_display_icon(self):
        color = "info"
        icon = "person-raised-hand"

        if self.is_private():
            color = "danger"

        if self.submission_type == FeedbackSubmissionType.BUG_REPORT:
            icon = "bug"

        return f"bi bi-{icon} text-{color}"
