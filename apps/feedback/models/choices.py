"""
Choices for the staff feedback triage system.

These mirror the string ENUM values written by the in-game `reports` command
(ishar-mud `rust-interop/src/feedback.rs`) and the Discord bridge. The values
are the literal strings stored in the shared `ishar` database, so they must not
drift from the game side.
"""
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class FeedbackType(TextChoices):
    """`feedback.feedback_type` ENUM('bug','typo','idea')."""

    BUG = "bug", _("Bug")
    TYPO = "typo", _("Typo")
    IDEA = "idea", _("Idea")


class FeedbackSource(TextChoices):
    """`feedback.source` ENUM('game','discord')."""

    GAME = "game", _("Game")
    DISCORD = "discord", _("Discord")


class FeedbackState(TextChoices):
    """`feedback.state` ENUM('open','in_progress','closed') — lifecycle axis."""

    OPEN = "open", _("Open")
    IN_PROGRESS = "in_progress", _("In Progress")
    CLOSED = "closed", _("Closed")


class FeedbackResolution(TextChoices):
    """`feedback.resolution` ENUM — closure reason, only set when closed."""

    FIXED = "fixed", _("Fixed")
    WONTFIX = "wontfix", _("Won't Fix")
    DUPLICATE = "duplicate", _("Duplicate")
    OTHER = "other", _("Other")


class CommentSource(TextChoices):
    """`feedback_comments.source` ENUM('game','discord','system')."""

    GAME = "game", _("Game")
    DISCORD = "discord", _("Discord")
    SYSTEM = "system", _("System")


class SyncAction(TextChoices):
    """
    Outbox verb — the staff action whose side-effects (Discord thread echoes,
    GitHub issue/comment/state) the host daemon must replay. These mirror the
    `reports` subcommands one-to-one; the daemon builds the exact Discord/GitHub
    payloads the in-game command would, so no presentation logic lives here.
    """

    ACK = "ack", _("Acknowledge")
    COMMENT = "comment", _("Comment")
    PROGRESS = "progress", _("Progress")
    RESOLVE = "resolve", _("Resolve")
    WONTFIX = "wontfix", _("Won't Fix")
    CLOSE = "close", _("Close")
    DUPLICATE = "dupe", _("Duplicate")
    REOPEN = "reopen", _("Reopen")
    BOUNTY = "bounty", _("Bounty")
    PROMOTE = "promote", _("Promote")
    ASSIGN_CLAUDE = "assign_claude", _("Assign to Claude")


class SyncStatus(TextChoices):
    """Outbox row lifecycle, drained by the host daemon."""

    PENDING = "pending", _("Pending")
    DONE = "done", _("Done")
    ERROR = "error", _("Error")
