from django.contrib.admin import StackedInline

from ...models.stat import MobileStat


class MobileStatAdminInline(StackedInline):
    """Mobile statistic flag inline administration."""
    model = MobileStat
    extra = 0
    verbose_name = "Statistic"

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
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
