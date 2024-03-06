from django.contrib import admin

from ..models.criteria import AchievementCriteria


@admin.register(AchievementCriteria)
class AchievementCriteriaAdmin(admin.ModelAdmin):
    """Ishar achievement criteria administration."""
    list_display = ("criteria_id", "criteria_type", "achievement",)
    list_display_links = ("criteria_id", "criteria_type",)
    list_filter = ("achievement", "criteria_type",)
    readonly_fields = ("criteria_id",)
    search_fields = ("description", "target_value",)

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
