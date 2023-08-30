from django.db import models

from .account import Account


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
        to=Account,
        on_delete=models.DO_NOTHING,
        help_text="Account that created the news post.",
        verbose_name="Account"
    )
    created_at = models.DateTimeField(
        help_text="Date and time when the news post was created.",
        verbose_name="Created At"
    )
    subject = models.CharField(
        max_length=64,
        help_text="Subject of the news post.",
        verbose_name="Subject"
    )
    body = models.TextField(
        help_text="Body of the news post.",
        verbose_name="Body"
    )

    class Meta:
        managed = False
        db_table = "news"
        ordering = ("-created_at", "-news_id", "account")
        verbose_name = "News"
        verbose_name_plural = "News"

    def __repr__(self):
        return (
            "News: "
            f"{repr(self.__str__())} @ {self.created_at} ({self.news_id})"
        )

    def __str__(self):
        return self.subject
