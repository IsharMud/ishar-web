from django.contrib import admin

from .inlines.desc import MobileDescriptionsTabularInline
from .inlines.flag import MobileFlagTabularInline

from ..models.mobile import Mobile


@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    """
    Ishar mobile administration.
    """
    list_display = ("id", "long_name", "level", "description")
    list_display_links = ("id", "long_name")
    list_filter = (
        "mob_class", "level", "race", "sex",
        ("spec_func", admin.EmptyFieldListFilter),
    )
    readonly_fields = ("id",)
    search_fields = (
        "id", "name", "long_name", "room_desc", "description", "spec_func"
    )
    inlines = (MobileDescriptionsTabularInline, MobileFlagTabularInline)
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
