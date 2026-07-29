from django.db import models

from .application import TrialApplication
from .choices import TrialCommentKind


class TrialComment(models.Model):
    """One timeline entry on an application: staff comment, applicant reply,
    or a system record of a state change (the audit trail)."""

    id = models.AutoField(
        primary_key=True,
        verbose_name="Comment ID",
    )
    application = models.ForeignKey(
        to=TrialApplication,
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comment",
        verbose_name="Application",
    )
    kind = models.CharField(
        max_length=16,
        choices=TrialCommentKind,
        verbose_name="Kind",
    )
    is_internal = models.BooleanField(
        default=False,
        help_text="Staff-only: never shown to the applicant, never echoed to Discord.",
        verbose_name="Internal?",
    )
    author = models.CharField(
        max_length=64,
        help_text="Staff name, or the applicant's character/account name.",
        verbose_name="Author",
    )
    body = models.TextField(
        verbose_name="Body",
    )
    created_at = models.DateTimeField(
        verbose_name="Created At",
    )

    class Meta:
        managed = True
        db_table = "trial_comments"
        ordering = ("id",)
        verbose_name = "Trial Comment"
        verbose_name_plural = "Trial Comments"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: #{self.pk} on #{self.application_id}"

    def __str__(self) -> str:
        return f"{self.author}: {self.body[:40]}"

    def is_system(self) -> bool:
        return self.kind == TrialCommentKind.SYSTEM

    @property
    def kind_icon(self) -> str:
        """Bootstrap-icons name for the timeline tile."""
        return {
            TrialCommentKind.STAFF: "shield-check",
            TrialCommentKind.APPLICANT: "person",
            TrialCommentKind.SYSTEM: "gear",
        }.get(self.kind, "chat")
