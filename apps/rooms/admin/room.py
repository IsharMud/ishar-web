from django.contrib import admin

from .inlines.room_exit import RoomExitStackedInline


class RoomAdmin(admin.ModelAdmin):
    """Ishar room administration."""

    list_display = (
        "vnum",
        "name",
        "description",
        "spec_func",
    )
    list_display_links = ("vnum", "name")
    list_filter = (
        "zone_id",
        "terrain",
        ("spec_func", admin.EmptyFieldListFilter),
        "is_deleted",
        "is_dirty",
    )
    inlines = (
        RoomExitStackedInline,
    )
    search_fields = (
        "vnum",
        "name",
        "spec_func",
    )
    show_full_result_count = True
    show_facets = admin.ShowFacets.ALWAYS

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
