"""
Timeline comment on a feedback report (`feedback_comments` table).

Game-owned table (`managed = False`). Rows come from three sources: in-game
staff comments (`game`), Discord replies ingested by the bridge (`discord`),
and `system` entries the game/website write to record staff actions
(acknowledged, promoted, closed, …). The website appends `game` staff comments
and `system` action entries; it never issues DDL here.
"""
from django.db import models

from apps.core.models.unsigned import UnsignedAutoField

from .choices import CommentSource
from .feedback import Feedback


class FeedbackComment(models.Model):
    """A single comment / timeline entry on a feedback report."""

    id = UnsignedAutoField(
        primary_key=True,
        db_column="id",
        help_text="Auto-generated permanent comment ID.",
        verbose_name="Comment ID",
    )
    feedback = models.ForeignKey(
        to=Feedback,
        db_column="feedback_id",
        to_field="id",
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comment",
        help_text="The report this comment belongs to.",
        verbose_name="Feedback Report",
    )
    source = models.CharField(
        max_length=8,
        db_column="source",
        choices=CommentSource,
        default=CommentSource.GAME,
        help_text="Origin of the comment: game, discord, or system.",
        verbose_name="Source",
    )
    author = models.CharField(
        max_length=64,
        db_column="author",
        help_text="Display name of the comment author.",
        verbose_name="Author",
    )
    is_staff = models.BooleanField(
        db_column="is_staff",
        default=False,
        help_text="Whether the author is staff.",
        verbose_name="Staff?",
    )
    body = models.TextField(
        db_column="body",
        help_text="The comment text.",
        verbose_name="Body",
    )
    discord_message_id = models.PositiveBigIntegerField(
        db_column="discord_message_id",
        blank=True,
        null=True,
        help_text="Discord message ID, for Discord-sourced comments.",
        verbose_name="Discord Message ID",
    )
    discord_author_id = models.PositiveBigIntegerField(
        db_column="discord_author_id",
        blank=True,
        null=True,
        help_text="Discord author ID, for Discord-sourced comments.",
        verbose_name="Discord Author ID",
    )
    created_at = models.DateTimeField(
        db_column="created_at",
        blank=True,
        null=True,
        help_text="When the comment was created.",
        verbose_name="Created At",
    )

    class Meta:
        managed = False
        db_table = "feedback_comments"
        ordering = ("id",)
        verbose_name = "Feedback Comment"
        verbose_name_plural = "Feedback Comments"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: #{self.pk} on #{self.feedback_id}"

    def __str__(self) -> str:
        return f"{self.author} ({self.source}) on #{self.feedback_id}"

    def is_system(self) -> bool:
        return self.source == CommentSource.SYSTEM

    def is_discord(self) -> bool:
        return self.source == CommentSource.DISCORD

    @property
    def source_icon(self) -> str:
        """Bootstrap-icons name marking where the comment came from."""
        return {
            CommentSource.GAME: "controller",
            CommentSource.DISCORD: "discord",
            CommentSource.SYSTEM: "gear",
        }.get(self.source, "chat")
