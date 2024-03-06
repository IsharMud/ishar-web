from django.contrib import admin

from ..models.reward import AchievementReward


@admin.register(AchievementReward)
class AchievementRewardAdmin(admin.ModelAdmin):
    """Ishar achievement reward administration."""
    list_display = ("reward_id", "reward_type", "achievement",)
    list_display_links = ("reward_id", "reward_type",)
    list_filter = ("achievement", "reward_type",)
    readonly_fields = ("reward_id",)
    search_fields = ("reward_value", "description",)

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return self.has_add_permission(request, obj)

    def has_delete_permission(self, request, obj=None) -> bool:
        return self.has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)
