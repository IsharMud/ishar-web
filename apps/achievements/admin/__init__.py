from django.contrib.admin import site

from ..models.achievement import Achievement
from ..models.class_restrict import AchievementClassRestrict
from ..models.criteria import AchievementCriteria
from ..models.reward import AchievementReward
from ..models.trigger import AchievementTrigger

from .achievement import AchievementAdmin
from .class_restrict import AchievementClassRestrictAdmin
from .criteria import AchievementCriteriaAdmin
from .reward import AchievementRewardAdmin
from .trigger import AchievementTriggerAdmin


site.register(Achievement, AchievementAdmin)
site.register(AchievementClassRestrict, AchievementClassRestrictAdmin)
site.register(AchievementCriteria, AchievementCriteriaAdmin)
site.register(AchievementReward, AchievementRewardAdmin)
site.register(AchievementTrigger, AchievementTriggerAdmin)
