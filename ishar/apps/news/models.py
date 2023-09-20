from django.db import models
from django.utils import timezone

from ishar.apps.accounts.models import Account


class News(models.Model):
    """
    News post.
    """
    news_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated permanent ID number of the news post.",
        verbose_name="News ID"
    )
    account = models.ForeignKey(
        db_column="account_id",
        to=Account,
        on_delete=models.DO_NOTHING,
        help_text="Account that created the news post.",
        verbose_name="Account"
    )
    created = models.DateTimeField(
        db_column="created",
        default=timezone.now,
        help_text="Date and time when the news post was created.",
        verbose_name="Created"
    )
    subject = models.CharField(
        db_column="subject",
        max_length=64,
        help_text="Subject of the news post.",
        verbose_name="Subject"
    )
    body = models.TextField(
        db_column="body",
        help_text="Body of the news post.",
        verbose_name="Body"
    )
    is_visible = models.BooleanField(
        db_column="is_visible",
        default=True,
        help_text="Should the news post be visible publicly?",
        verbose_name="Visible?"
    )

    class Meta:
        managed = True
        db_table = "news"
        default_related_name = "news"
        ordering = ("-created", "-news_id")
        verbose_name = "News"
        verbose_name_plural = "News"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}: "
            f"{repr(self.__str__())} @ {self.created} ({self.news_id}) "
            f"[by {self.account.account_name}]"
        )

    def __str__(self):
        return self.subject
