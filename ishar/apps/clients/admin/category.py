from django.contrib.admin import ModelAdmin, register

from ishar.apps.clients.models.category import MUDClientCategory


@register(MUDClientCategory)
class MUDClientCategoryAdmin(ModelAdmin):
    """
    MUD client category administration.
    """
    fields = list_display = ("name", "is_visible", "display_order")
    list_filter = ("is_visible",)
    readonly_fields = ("category_id",)
    search_fields = ("name",)

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
        if request.user and not request.user.is_anonymous:
            if request.user.is_god():
                return True
        return False

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False
