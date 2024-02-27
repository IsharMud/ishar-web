from django.db import models
from django.urls import reverse

from ishar.apps.accounts.models import Account


class FAQ(models.Model):
    """
    Frequently Asked Question.
    """
    faq_id = models.AutoField(
        blank=False,
        help_text="Auto-generated permanent ID number of the question.",
        null=False,
        primary_key=True,
        verbose_name="FAQ ID"
    )
    slug = models.SlugField(
        default=None,
        help_text="Short (slug) name for the HTML anchor/URL.",
        max_length=16,
        unique=True,
        verbose_name="(Slug) Name"
    )
    account = models.ForeignKey(
        db_column="account_id",
        blank=False,
        help_text="Account that created the question.",
        null=False,
        on_delete=models.DO_NOTHING,
        to=Account,
        verbose_name="Account"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        db_column="created",
        help_text="Date and time when the question was created.",
        null=False,
        verbose_name="Created"
    )
    question_text = models.TextField(
        blank=False,
        db_column="question_text",
        help_text="Text of the question.",
        null=False,
        verbose_name="Question"
    )
    question_answer = models.TextField(
        blank=False,
        db_column="question_answer",
        help_text="Answer to the question.",
        null=False,
        verbose_name="Answer"
    )
    is_visible = models.BooleanField(
        blank=False,
        db_column="is_visible",
        default=True,
        help_text="Should the question be visible publicly?",
        null=False,
        verbose_name="Visible?"
    )
    display_order = models.PositiveIntegerField(
        db_column="display_order",
        null=False,
        blank=False,
        unique=True,
        help_text="What is the numeric display order of the question?",
        verbose_name="Display Order"
    )

    class Meta:
        managed = True
        db_table = "faqs"
        default_related_name = "faqs"
        ordering = ("display_order",)
        verbose_name = "Frequently Asked Question"
        verbose_name_plural = "Frequently Asked Questions"

    def get_absolute_url(self) -> str:
        """Anchored URL to FAQ page."""
        return reverse(viewname="faq") + "#" + self.slug

    def __repr__(self):
        return "%s: %s (%i)" % (
            self.__class__.__name__, self.__str__(), self.pk
        )

    def __str__(self):
        return self.slug
