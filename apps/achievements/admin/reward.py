from django.contrib.admin import ModelAdmin, register

from ..models.reward import AchievementReward


@register(AchievementReward)
class AchievementRewardAdmin(ModelAdmin):
    """Ishar achievement reward administration."""
    list_display = ("reward_id", "reward_type", "achievement",)
    list_display_links = ("reward_id", "reward_type",)
    list_filter = ("achievement", "reward_type",)
    readonly_fields = ("reward_id",)
    search_fields = ("reward_value",)

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return self.has_add_permission(request, obj)

    def has_delete_permission(self, request, obj=None) -> bool:
        return self.has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)
