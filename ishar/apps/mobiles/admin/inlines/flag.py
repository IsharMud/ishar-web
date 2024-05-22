from django.contrib.admin import TabularInline

from ...models.flag import MobileFlag


class MobileFlagTabularInline(TabularInline):
    """Mobile player flag tabular inline administration."""
    model = MobileFlag
    extra = 1
    fields = ("flag", "value")
    ordering = ("-value", "flag__name")
    verbose_name = "Flag"
    verbose_name_plural = "Flags"

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            if request.user.is_god():
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
