from django.contrib import admin

from ..models.class_restrict import AchievementClassRestrict


@admin.register(AchievementClassRestrict)
class AchievementClassRestrictAdmin(admin.ModelAdmin):
    """Ishar achievement class restriction administration."""
    list_display = ("acr_id", "player_class", "achievement",)
    list_filter = ("achievement", "player_class",)
    readonly_fields = ("acr_id",)
    search_fields = ("achievement", "player_class")

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
