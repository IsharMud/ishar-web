from django.contrib import admin

from .inlines.class_restrict import AchievementClassRestrictTabularInline
from .inlines.criteria import AchievementCriteriaTabularInline
from .inlines.reward import AchievementRewardTabularInline
from .inlines.trigger import AchievementTriggerTabularInline
from ..models.achievement import Achievement


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    """Ishar achievement administration."""
    inlines = (
        AchievementClassRestrictTabularInline,
        AchievementCriteriaTabularInline,
        AchievementRewardTabularInline,
        AchievementTriggerTabularInline,
    )
    list_display = ("achievement_id", "name", "description", "is_hidden")
    list_filter = (
        "criteria_type", "category", "parent_category", "is_hidden",
        "ordinal", "created_at", "updated_at",
    )
    readonly_fields = ("achievement_id", "created_at", "updated_at")
    search_fields = ("name", "description")

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
