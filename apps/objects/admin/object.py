from django.contrib import admin

from .inlines import ObjectAffectFlagInline, ObjectExtraInline, \
    ObjectFlagInline, ObjectObjectModInline, ObjectWearableFlagInline

from ..models.object import Object


@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    """Ishar object administration."""
    date_hierarchy = "updated_at"
    list_display = ("vnum", "display", "appearance", "description")
    list_display_links = ("vnum", "display")
    list_filter = (
        "deleted", "item_type",
        ("enchant", admin.RelatedOnlyFieldListFilter),
        ("grant_skill", admin.RelatedOnlyFieldListFilter),
        ("appearance", admin.EmptyFieldListFilter),
        ("description", admin.EmptyFieldListFilter),
        ("func", admin.EmptyFieldListFilter),
        ("extra", admin.EmptyFieldListFilter),
        "flag__artifact", "flag__relic",
        "created_at", "updated_at"
    )
    inlines = (
        ObjectAffectFlagInline, ObjectExtraInline, ObjectFlagInline,
        ObjectObjectModInline, ObjectWearableFlagInline
    )
    readonly_fields = ("vnum", "display", "created_at", "updated_at")
    search_fields = (
        "vnum", "name", "longname", "appearance", "description", "func",
    )
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
