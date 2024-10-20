from django.contrib.admin import TabularInline


class BaseQuestTabularInline(TabularInline):
    """Base quest inline tabular administration."""

    extra = 1
    model = None

    def has_add_permission(self, request, obj) -> bool:
        return self.has_module_permission(request)

    def has_change_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request)

    def has_delete_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request)

    def has_module_permission(self, request) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request)
