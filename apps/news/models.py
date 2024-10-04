from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Account


class NewsManager(models.Manager):
    def get_by_natural_key(self, subject):
        # Natural key is news post subject.
        return self.get(subject=subject)


class News(models.Model):
    """Ishar website news post."""

    news_id = models.AutoField(
        primary_key=True,
        help_text=_("Auto-generated permanent ID number of the news post."),
        verbose_name=_("News ID")
    )
    account = models.ForeignKey(
        db_column="account_id",
        to=Account,
        on_delete=models.DO_NOTHING,
        help_text=_("Account that created the news post."),
        verbose_name=_("Account")
    )
    created = models.DateTimeField(
        db_column="created",
        default=now,
        help_text=_("Date and time when the news post was created."),
        verbose_name=_("Created")
    )
    subject = models.CharField(
        db_column="subject",
        max_length=64,
        help_text=_("Subject of the news post."),
        verbose_name=_("Subject")
    )
    body = models.TextField(
        db_column="body",
        help_text=_("Body of the news post."),
        verbose_name=_("Body")
    )
    is_visible = models.BooleanField(
        db_column="is_visible",
        default=True,
        help_text=_("Should the news post be visible publicly?"),
        verbose_name=_("Visible?")
    )

    class Meta:
        managed = True
        db_table = "news"
        default_related_name = "news"
        get_latest_by = ("is_visible", "created")
        ordering = ("-created", "-news_id")
        verbose_name = _("News Post")
        verbose_name_plural = _("News Posts")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.subject

    def natural_key(self):
        # Natural key is news post subject.
        return self.subject
