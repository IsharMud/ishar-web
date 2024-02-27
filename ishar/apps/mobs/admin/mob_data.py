from django.contrib import admin

from ..models.mob_data import MobData


@admin.register(MobData)
class MobDataAdmin(admin.ModelAdmin):
    """
    Ishar mob data administration.
    """
    list_display = ("id", "long_name", "level", "description")
    list_display_links = ("id", "long_name")
    list_filter = (
        "level", "mob_class", "race", "sex",
        ("spec_func", admin.EmptyFieldListFilter),
    )
    readonly_fields = ("id",)
    search_fields = (
        "name", "long_name", "room_desc", "description", "spec_func"
    )
    show_full_result_count = True
    show_facets = admin.ShowFacets.ALWAYS

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
