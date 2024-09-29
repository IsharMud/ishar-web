from django.contrib import admin

from apps.players.models.object import PlayerObject


@admin.register(PlayerObject)
class PlayerObjectAdmin(admin.ModelAdmin):
    """Player objects administration."""
    model = PlayerObject
    fieldsets = (
        (None, {"fields": ("player_objects_id",)}),
        ("Player", {"fields": ("player",)}),
        ("Object", {"fields": ("object",)}),
        ("Position", {"fields": ("position_type", "position_val",)}),
        ("Container", {"fields": ("parent_player_object",)}),
        ("Details", {
            "fields": ("enchant", "timer", "state", "bound", "min_level")
        }),
        ("Values", {"fields": ("val0", "val1", "val2", "val3")}),
    )
    list_display = ("player", "object", "position_type", "position_val")
    list_display_links = ("player", "object")
    list_filter = (
        ("player", admin.RelatedOnlyFieldListFilter),
        "position_type",
        "position_val",
        ("parent_player_object", admin.EmptyFieldListFilter),
        "enchant", "min_level",
        "object__flag__artifact", "object__flag__relic"
    )
    readonly_fields = ("player_objects_id",)
    search_fields = (
        "player__name", "object__vnum", "object__name", "object__longname"
    )
    show_facets = admin.ShowFacets.ALWAYS
    verbose_name = "Player Object"
    verbose_name_plural = "Player's Objects"

    def has_add_permission(self, request) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_module_permission(self, request) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False
