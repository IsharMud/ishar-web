from ...models.reward import QuestReward

from . import BaseQuestTabularInline


class QuestRewardTabularInline(BaseQuestTabularInline):
    """Quest reward inline tabular administration."""
    model = QuestReward
