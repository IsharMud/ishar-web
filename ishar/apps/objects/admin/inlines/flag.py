from django.contrib.admin import StackedInline

from ...models.flag import ObjectFlag


class ObjectFlagTabularInline(StackedInline):
    """Object flag tabular inline administration."""
    model = ObjectFlag
    extra = 1
    readonly_fields = ("created_at", "updated_at")

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
