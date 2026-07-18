"""
Survey structure: sections, questions, and their options.

One `SurveyOption` model serves two roles, split by `is_matrix_row`:
answerable choices (single/multi/rank picks, or a matrix's rating scale) and
matrix *rows* (the items being rated). Non-matrix kinds only use choices.
"""
from django.db import models

from .survey import Survey


class QuestionKind(models.TextChoices):
    SINGLE = "single", "Single choice"
    MULTI = "multi", "Multiple choice"
    MATRIX = "matrix", "Matrix (rate each row)"
    RANK = "rank", "Ranked picks"
    TEXT = "text", "Free text"


class SurveySection(models.Model):
    """A titled group of questions, with an optional preamble."""

    section_id = models.AutoField(
        primary_key=True,
        verbose_name="Section ID",
    )
    survey = models.ForeignKey(
        to=Survey,
        on_delete=models.CASCADE,
        related_name="sections",
        related_query_name="section",
        verbose_name="Survey",
    )
    position = models.PositiveSmallIntegerField(
        default=0,
        help_text="Order of the section within the survey.",
        verbose_name="Position",
    )
    title = models.CharField(
        max_length=128,
        help_text="Section heading.",
        verbose_name="Title",
    )
    preamble = models.TextField(
        blank=True,
        default="",
        help_text="Optional framing text shown under the section heading.",
        verbose_name="Preamble",
    )

    class Meta:
        managed = True
        db_table = "survey_sections"
        ordering = ("survey", "position", "section_id")
        verbose_name = "Survey Section"
        verbose_name_plural = "Survey Sections"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.title


class SurveyQuestion(models.Model):
    """A single question within a survey."""

    question_id = models.AutoField(
        primary_key=True,
        verbose_name="Question ID",
    )
    survey = models.ForeignKey(
        to=Survey,
        on_delete=models.CASCADE,
        related_name="questions",
        related_query_name="question",
        verbose_name="Survey",
    )
    section = models.ForeignKey(
        to=SurveySection,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="questions",
        related_query_name="question",
        help_text="Section this question appears under (optional).",
        verbose_name="Section",
    )
    position = models.PositiveSmallIntegerField(
        default=0,
        help_text="Order of the question within its section.",
        verbose_name="Position",
    )
    kind = models.CharField(
        max_length=8,
        choices=QuestionKind,
        default=QuestionKind.SINGLE,
        verbose_name="Kind",
    )
    text = models.CharField(
        max_length=255,
        help_text="The question itself.",
        verbose_name="Question",
    )
    hint = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Optional helper text shown under the question.",
        verbose_name="Hint",
    )
    required = models.BooleanField(
        default=True,
        help_text="Whether an answer is required to submit the survey.",
        verbose_name="Required?",
    )
    max_choices = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text=(
            "Multiple choice: maximum picks allowed (blank = unlimited). "
            "Ranked picks: how many ranked slots (e.g. 2 = rank your top 2)."
        ),
        verbose_name="Max Choices",
    )
    allow_other = models.BooleanField(
        default=False,
        help_text='Offer an "Other: ___" write-in alongside the options.',
        verbose_name='Allow "Other"?',
    )

    class Meta:
        managed = True
        db_table = "survey_questions"
        ordering = ("survey", "section__position", "position", "question_id")
        verbose_name = "Survey Question"
        verbose_name_plural = "Survey Questions"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.text

    # Options are always prefetched whole (tiny sets); these filter in Python
    # so a prefetch_related("options") serves both without extra queries.

    @property
    def choices(self) -> list:
        """Answerable options (for matrix questions: the rating scale)."""
        return [o for o in self.options.all() if not o.is_matrix_row]

    @property
    def matrix_rows(self) -> list:
        """The rated items of a matrix question."""
        return [o for o in self.options.all() if o.is_matrix_row]

    @property
    def rank_slots(self) -> range:
        """1-based ranked-pick slots (rank kind), e.g. range(1, 3) for top 2."""
        limit = self.max_choices or len(self.choices)
        return range(1, limit + 1)


class SurveyOption(models.Model):
    """One option of a question: an answerable choice or a matrix row."""

    option_id = models.AutoField(
        primary_key=True,
        verbose_name="Option ID",
    )
    question = models.ForeignKey(
        to=SurveyQuestion,
        on_delete=models.CASCADE,
        related_name="options",
        related_query_name="option",
        verbose_name="Question",
    )
    position = models.PositiveSmallIntegerField(
        default=0,
        help_text="Order of the option within the question.",
        verbose_name="Position",
    )
    text = models.CharField(
        max_length=255,
        verbose_name="Text",
    )
    is_matrix_row = models.BooleanField(
        default=False,
        help_text=(
            "Matrix questions only: this option is a rated row rather than a "
            "point on the rating scale."
        ),
        verbose_name="Matrix Row?",
    )

    class Meta:
        managed = True
        db_table = "survey_options"
        ordering = ("question", "position", "option_id")
        verbose_name = "Survey Option"
        verbose_name_plural = "Survey Options"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.text
