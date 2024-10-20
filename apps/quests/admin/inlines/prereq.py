from ...models.prereq import QuestPrereq

from . import BaseQuestTabularInline


class QuestPrereqTabularInline(BaseQuestTabularInline):
    """Quest pre-requisite inline tabular administration."""

    model = QuestPrereq
    fk_name = "quest"
