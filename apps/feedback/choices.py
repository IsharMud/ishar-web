from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


"""Feedback submission type choices."""

class FeedbackSubmissionTypePublic(IntegerChoices):

    BUG_REPORT = 1
    IDEA = 2, _("Idea / Suggestion")


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.value})"

    def __str__(self) -> str:
        return self.name.replace("_", " ").title()


class FeedbackSubmissionType(IntegerChoices):

    COMPLETE = -1
    OTHER = 0
    BUG_REPORT = 1
    IDEA = 2, _("Idea / Suggestion")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.value})"

    def __str__(self) -> str:
        return self.name.replace("_", " ").title()
