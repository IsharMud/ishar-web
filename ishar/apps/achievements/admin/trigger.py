from django.contrib.admin import ModelAdmin, register

from ..models.trigger import AchievementTrigger


@register(AchievementTrigger)
class AchievementTriggerAdmin(ModelAdmin):
    """Ishar trigger reward administration."""
    list_display = ("achievement_triggers_id", "trigger_type", "achievement",)
    list_display_links = ("achievement_triggers_id", "trigger_type",)
    list_filter = ("achievement", "trigger_type",)
    readonly_fields = ("achievement_triggers_id",)

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
