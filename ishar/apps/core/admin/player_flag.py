from django.contrib.admin import ModelAdmin, register

from ..models.player_flag import PlayerFlag


@register(PlayerFlag)
class PlayerFlagAdmin(ModelAdmin):
    """Player flag administration."""
    model = PlayerFlag
    fieldsets = ((None, {"fields": ("flag_id", "name")}),)
    list_display = list_display_links = search_fields = ("flag_id", "name",)
    readonly_fields = ("flag_id",)
    verbose_name = "Player's Flag"
    verbose_name_plural = "Player's Flags"

    def has_add_permission(self, request) -> bool:
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
