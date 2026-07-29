"""Context processor: trial-application badges for the nav/portal pills."""
from django.db import DatabaseError


def trials_badges(request):
    """
    `TRIALS_PENDING`: applications under review (Eternal+ only — the count
    reveals staff-queue state). `TRIAL_ATTENTION`: the account has an
    application sent back for revision. Defensively zero if the trial tables
    aren't migrated yet.
    """
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return {"TRIALS_PENDING": 0, "TRIAL_ATTENTION": False}
    try:
        from .models import TrialApplication, TrialStatus
        pending = 0
        if user.is_eternal():
            pending = TrialApplication.objects.filter(
                status=TrialStatus.SUBMITTED,
            ).count()
        attention = TrialApplication.objects.filter(
            account=user, status=TrialStatus.NEEDS_REVISION,
        ).exists()
        return {"TRIALS_PENDING": pending, "TRIAL_ATTENTION": attention}
    except DatabaseError:
        return {"TRIALS_PENDING": 0, "TRIAL_ATTENTION": False}
