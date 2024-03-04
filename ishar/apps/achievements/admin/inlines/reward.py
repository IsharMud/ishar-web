from django.contrib.admin import TabularInline

from ...models.reward import AchievementReward


class AchievementRewardTabularInline(TabularInline):
    """Achievement reward tabular inline administration."""
    extra = 1
    model = AchievementReward
    verbose_name = "Reward"
    verbose_name_plural = "Rewards"

    def has_add_permission(self, request, obj) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_module_permission(self, request) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False
