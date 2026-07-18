"""Context processor: open-survey count for the nav/portal pill."""
from django.db import DatabaseError


def surveys_open(request):
    """
    `SURVEYS_OPEN`: how many accepting surveys the logged-in account has not
    answered yet. Zero for anonymous users, and defensively zero if the survey
    tables aren't migrated yet.
    """
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return {"SURVEYS_OPEN": 0}
    try:
        from .models import Survey, SurveyState
        count = sum(
            1 for survey in Survey.objects.filter(
                status=SurveyState.OPEN,
            ).exclude(
                submission__account=user.account_id,
            )
            if survey.is_accepting()
        )
        return {"SURVEYS_OPEN": count}
    except DatabaseError:
        return {"SURVEYS_OPEN": 0}
