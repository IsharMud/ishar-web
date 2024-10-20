from ...models.step import QuestStep

from . import BaseQuestTabularInline


class QuestStepTabularInline(BaseQuestTabularInline):
    """Quest step inline tabular administration."""

    model = QuestStep
