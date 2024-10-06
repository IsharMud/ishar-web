from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Account

from .submission import FeedbackSubmission


class FeedbackCommentManager(models.Manager):
    def get_by_natural_key(self, comment_id):
        # Natural key has to be the ID.
        return self.get(comment_id=comment_id)


class FeedbackComment(models.Model):
    """Ishar website feedback comment."""

    objects = FeedbackCommentManager()

    comment_id = models.AutoField(
        blank=False,
        db_column="comment_id",
        help_text=_(
            "Auto-generated permanent ID number of the feedback comment."
        ),
        null=False,
        primary_key=True,
        verbose_name=_("Comment ID")
    )
    feedback_submission = models.ForeignKey(
        db_column="submission_id",
        blank=False,
        help_text=_("Account that submitted the feedback comment."),
        null=False,
        on_delete=models.DO_NOTHING,
        to=FeedbackSubmission,
        to_field="submission_id",
        verbose_name=_("Feedback Submission")
    )
    body_text = models.TextField(
        blank=False,
        db_column="body_text",
        help_text=_("Body text of the feedback comment."),
        null=False,
        verbose_name=_("Message")
    )
    account = models.ForeignKey(
        db_column="account_id",
        blank=False,
        help_text=_("Account that submitted the feedback comment."),
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
        help_text=_("Date and time when the comment was submitted."),
        null=False,
        verbose_name=_("Submitted")
    )

    class Meta:
        managed = True
        db_table = "feedback_comments"
        default_related_name = "comment"
        get_latest_by = ("submitted",)
        ordering = ("-submitted",)
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def natural_key(self) -> id:
        # Natural key has to be the ID.
        return self.comment_id
