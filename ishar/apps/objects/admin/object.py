from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html

from ..models.object import Object


@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    """Ishar mobile administration."""
    list_display = ("vnum", "longname", "appearance", "description", "state")
    list_display_links = ("vnum", "longname")
    list_filter = (
        "deleted",
        ("enchant", admin.RelatedOnlyFieldListFilter),
        ("appearance", admin.EmptyFieldListFilter),
        ("description", admin.EmptyFieldListFilter),
        ("func", admin.EmptyFieldListFilter),
    )
    readonly_fields = ("vnum",)
    search_fields = (
        "vnum", "name", "longname", "appearance", "description", "func",
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
