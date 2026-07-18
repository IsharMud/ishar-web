"""
Survey responses: one submission per account per survey, answers normalized
one row per datum:

- single / text:  one row (option or text)
- multi:          one row per pick; an "Other" write-in is option=None + text
- matrix:         one row per rated row (row + option)
- rank:           one row per ranked pick (option/text + rank, 1-based)

The account FK is Django-level only (`db_constraint=False`) — the game owns
the accounts table and its constraints must stay untouched.
"""
from django.db import models

from apps.accounts.models import Account

from .question import SurveyOption, SurveyQuestion
from .survey import Survey


class SurveySubmission(models.Model):
    """One account's completed response to a survey."""

    submission_id = models.AutoField(
        primary_key=True,
        verbose_name="Submission ID",
    )
    survey = models.ForeignKey(
        to=Survey,
        on_delete=models.CASCADE,
        related_name="submissions",
        related_query_name="submission",
        verbose_name="Survey",
    )
    account = models.ForeignKey(
        to=Account,
        db_column="account_id",
        to_field="account_id",
        db_constraint=False,
        on_delete=models.CASCADE,
        related_name="survey_submissions",
        related_query_name="survey_submission",
        verbose_name="Account",
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Submitted At",
    )

    class Meta:
        managed = True
        db_table = "survey_submissions"
        constraints = (
            models.UniqueConstraint(
                fields=("survey", "account"),
                name="one_submission_per_account",
            ),
        )
        ordering = ("-submission_id",)
        verbose_name = "Survey Submission"
        verbose_name_plural = "Survey Submissions"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return f"{self.account} → {self.survey}"


class SurveyAnswer(models.Model):
    """A single answer datum within a submission."""

    answer_id = models.AutoField(
        primary_key=True,
        verbose_name="Answer ID",
    )
    submission = models.ForeignKey(
        to=SurveySubmission,
        on_delete=models.CASCADE,
        related_name="answers",
        related_query_name="answer",
        verbose_name="Submission",
    )
    question = models.ForeignKey(
        to=SurveyQuestion,
        on_delete=models.CASCADE,
        related_name="answers",
        related_query_name="answer",
        verbose_name="Question",
    )
    option = models.ForeignKey(
        to=SurveyOption,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="answers",
        related_query_name="answer",
        help_text="The picked choice (None for free text / an Other write-in).",
        verbose_name="Option",
    )
    row = models.ForeignKey(
        to=SurveyOption,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="row_answers",
        related_query_name="row_answer",
        help_text="Matrix questions only: the row this rating applies to.",
        verbose_name="Matrix Row",
    )
    rank = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="Ranked picks only: 1 = first pick.",
        verbose_name="Rank",
    )
    text = models.TextField(
        blank=True,
        default="",
        help_text='Free-text answer or an "Other" write-in.',
        verbose_name="Text",
    )

    class Meta:
        managed = True
        db_table = "survey_answers"
        ordering = ("submission", "question", "rank", "answer_id")
        verbose_name = "Survey Answer"
        verbose_name_plural = "Survey Answers"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return f"#{self.submission_id} Q{self.question_id}"

    @property
    def display_value(self) -> str:
        """Human-readable value for staff views and CSV export."""
        if self.option_id:
            return self.option.text
        if self.text:
            return f"Other: {self.text}" if self.question.kind != "text" else self.text
        return "—"
