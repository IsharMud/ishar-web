from django.contrib import admin

from ..models.mod import ObjectMod


@admin.register(ObjectMod)
class ObjectModAdmin(admin.ModelAdmin):
    """Ishar object mod administration."""
    date_hierarchy = "updated_at"
    list_display = list_display_links = ("mod_id", "name")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("mod_id", "created_at", "updated_at")
    search_fields = ("mod_id", "name")
    show_full_result_count = True
    show_facets = admin.ShowFacets.ALWAYS

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
        if request.user and not request.user.is_anonymous:
            if request.user.is_forger():
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
