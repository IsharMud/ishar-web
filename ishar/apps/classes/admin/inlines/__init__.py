from django.contrib.admin import TabularInline


class BaseClassTabularInline(TabularInline):
    """Base class inline tabular administration."""
    extra = 1
    model = None

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        return self.has_module_permission(request, obj)

    def has_delete_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False
