from django.contrib.admin import TabularInline

from ...models.player_flag import MobilePlayerFlag


class MobilePlayerFlagTabularInline(TabularInline):
    """Mobile player flag tabular inline administration."""

    model = MobilePlayerFlag
    extra = 1
    fields = ("player_flag", "value")
    ordering = ("-value", "player_flag__name")
    verbose_name = "Player Flag"
    verbose_name_plural = "Player Flags"

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            if request.user.is_forger():
                return True
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False
