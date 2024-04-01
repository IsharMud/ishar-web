from django.contrib.admin import TabularInline

from ...models.affect_flag import MobileAffectFlag


class MobileAffectFlagTabularInline(TabularInline):
    """Mobile affect flag tabular inline administration."""
    model = MobileAffectFlag
    extra = 1
    fields = ("affect_flag", "value")
    ordering = ("-value", "affect_flag__name")
    verbose_name = "Affect Flag"
    verbose_name_plural = "Affect Flags"

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
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
