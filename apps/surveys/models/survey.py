"""
Site-owned player survey (`surveys` table, `managed = True`).

A survey's lifecycle is a manual master switch (`status`) optionally narrowed
by a schedule window: it only accepts submissions while OPEN *and* inside
[opens_at, closes_at). Draft surveys are invisible to players (404, per the
site's gating convention).
"""
from django.db import models
from django.urls import reverse
from django.utils import timezone


class SurveyState(models.TextChoices):
    DRAFT = "draft", "Draft"
    OPEN = "open", "Open"
    CLOSED = "closed", "Closed"


class Survey(models.Model):
    """A player survey: sections of questions, one submission per account."""

    survey_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated ID number of the survey.",
        verbose_name="Survey ID",
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
        help_text="URL identifier of the survey (/surveys/<slug>/).",
        verbose_name="Slug",
    )
    title = models.CharField(
        max_length=128,
        help_text="Title of the survey.",
        verbose_name="Title",
    )
    intro = models.TextField(
        blank=True,
        default="",
        help_text="Introduction shown above the survey form.",
        verbose_name="Introduction",
    )
    status = models.CharField(
        max_length=8,
        choices=SurveyState,
        default=SurveyState.DRAFT,
        help_text=(
            "Draft surveys are invisible to players; only Open surveys accept "
            "submissions (further narrowed by the schedule window, if set)."
        ),
        verbose_name="Status",
    )
    opens_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Optional: while Open, accept no submissions before this time.",
        verbose_name="Opens At",
    )
    closes_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Optional: while Open, accept no submissions from this time on.",
        verbose_name="Closes At",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
    )

    class Meta:
        managed = True
        db_table = "surveys"
        default_related_name = "surveys"
        ordering = ("-survey_id",)
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse(viewname="survey", kwargs={"slug": self.slug})

    def get_admin_url(self) -> str:
        return reverse(
            viewname="admin:surveys_survey_change",
            args=(self.survey_id,)
        )

    # -- Lifecycle --------------------------------------------------------

    def is_draft(self) -> bool:
        return self.status == SurveyState.DRAFT

    def is_accepting(self) -> bool:
        """Whether a submission would be accepted right now."""
        if self.status != SurveyState.OPEN:
            return False
        now = timezone.now()
        if self.opens_at and now < self.opens_at:
            return False
        if self.closes_at and now >= self.closes_at:
            return False
        return True

    @property
    def state_label(self) -> str:
        """Effective state: the status refined by the schedule window."""
        if self.status == SurveyState.DRAFT:
            return "Draft"
        if self.status == SurveyState.CLOSED:
            return "Closed"
        now = timezone.now()
        if self.opens_at and now < self.opens_at:
            return "Scheduled"
        if self.closes_at and now >= self.closes_at:
            return "Closed"
        return "Open"

    @property
    def state_pill(self) -> str:
        """Admin Console pill modifier (.ac-pill--*) for the state."""
        return {
            "Draft": "warn",
            "Scheduled": "info",
            "Open": "ok",
            "Closed": "muted",
        }[self.state_label]
