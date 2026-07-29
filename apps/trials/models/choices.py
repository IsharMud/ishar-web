from django.db.models import TextChoices


class TrialStatus(TextChoices):
    """Application lifecycle. Open = SUBMITTED or NEEDS_REVISION; the rest are
    terminal and free the account's one-open-application slot."""

    SUBMITTED = "submitted", "Under Review"
    NEEDS_REVISION = "needs_revision", "Needs Revision"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"
    WITHDRAWN = "withdrawn", "Withdrawn"


# The two open states, in query-ready form.
OPEN_STATUSES = (TrialStatus.SUBMITTED, TrialStatus.NEEDS_REVISION)


class TrialTrack(TextChoices):
    ZONER = "zoner", "Zoner"
    CODER = "coder", "Coder"


class TrialCommentKind(TextChoices):
    STAFF = "staff", "Staff"
    APPLICANT = "applicant", "Applicant"
    SYSTEM = "system", "System"


class TrialSyncAction(TextChoices):
    """Semantic verbs the host daemon turns into staff-Discord posts."""

    SUBMITTED = "submitted"
    RESUBMITTED = "resubmitted"
    COMMENT = "comment"
    REPLY = "reply"
    NEEDS_REVISION = "needs_revision"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class TrialSyncStatus(TextChoices):
    PENDING = "pending"
    DONE = "done"
    ERROR = "error"
