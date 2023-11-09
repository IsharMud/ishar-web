from django.contrib import admin

from ishar.apps.clients.models import MUDClientCategory, MUDClient


@admin.register(MUDClientCategory)
class MUDClientCategoryAdmin(admin.ModelAdmin):
    """
    Ishar MUD client category administration.
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


@admin.register(MUDClient)
class MUDClientAdmin(admin.ModelAdmin):
    """
    Ishar MUD client administration.
    """
    fields = ("name", "category", "url", "is_visible")
    list_display = ("name", "get_category_link", "is_visible")
    list_filter = ("category", "is_visible")
    list_select_related = ("category",)
    readonly_fields = ("client_id",)
    search_fields = ("category", "name", "url")

    @admin.display(description="Category", ordering="category")
    def get_category_link(self, obj=None) -> str:
        if obj and obj.category:
            return obj.category.get_admin_link()
        return ''

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
