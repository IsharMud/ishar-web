from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Account

from .submission import FeedbackSubmission


class FeedbackVoteManager(models.Manager):
    def get_by_natural_key(self, vote_id):
        # Natural key has to be the ID.
        return self.get(vote_id=vote_id)


class FeedbackVote(models.Model):
    """Ishar website feedback vote."""

    objects = FeedbackVoteManager()

    vote_id = models.AutoField(
        blank=False,
        db_column="vote_id",
        help_text=_(
            "Auto-generated permanent ID number of the feedback vote."
        ),
        null=False,
        primary_key=True,
        verbose_name=_("Vote ID")
    )
    feedback_submission = models.ForeignKey(
        db_column="submission_id",
        blank=False,
        help_text=_("Feedback submission that was voted on."),
        null=False,
        on_delete=models.CASCADE,
        to=FeedbackSubmission,
        to_field="submission_id",
        verbose_name=_("Feedback Submission")
    )
    vote_value = models.BooleanField(
        blank=False,
        db_column="vote_value",
        help_text=_(
            "Positive (True) or negative (False) boolean value of the vote."
        ),
        null=False,
        verbose_name=_("Value")
    )
    account = models.ForeignKey(
        db_column="account_id",
        blank=False,
        help_text=_("Account that voted on the feedback submission."),
        null=False,
        on_delete=models.CASCADE,
        to=Account,
        to_field="account_id",
        verbose_name=_("Account")
    )
    voted = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        db_column="voted",
        help_text=_("Date and time of the vote."),
        null=False,
        verbose_name=_("Voted")
    )

    class Meta:
        managed = True
        constraints = (
            models.constraints.UniqueConstraint(
                fields=("account", "feedback_submission"),
                name="one_vote_per"
            ),
        )
        db_table = "feedback_votes"
        default_related_name = "votes"
        get_latest_by = ("voted",)
        ordering = ("-voted",)
        unique_together = ("account", "feedback_submission")
        verbose_name = "Vote"
        verbose_name_plural = "Votes"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} [{self.pk}]"

    def __str__(self) -> str:
        return (
            f"{self.vote_value} by {self.account}"
            f" @ {self.feedback_submission}"
        )

    def natural_key(self) -> int:
        # Natural key has to be the ID.
        return self.vote_id
