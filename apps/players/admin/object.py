from django.contrib import admin


class PlayerObjectContainedListFilter(admin.SimpleListFilter):
    title = "Contained?"
    parameter_name = "contained"

    def lookups(self, request, model_admin):
        return (
            ("1", "Yes"),
            ("0", "No")
        )

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == "1":
                queryset = queryset.exclude(parent_player_object__exact=0)
            if self.value() == "0":
                queryset = queryset.filter(parent_player_object__exact=0)
        return queryset


class PlayerObjectAdmin(admin.ModelAdmin):
    """Player objects administration."""

    fieldsets = (
        (None, {"fields": (
            "player_objects_id", "player", "object", "parent_player_object"
        )}),
        ("Position", {"fields": ("position_type", "position_val",)}),
        ("Details", {"fields": (
            "enchant", "timer", "state", "bound", "min_level"
        )}),
        ("Values", {"fields": ("val0", "val1", "val2", "val3")}),
    )
    list_display = ("__str__", "position_type", "position_val", "is_contained")
    list_filter = (
        ("player", admin.RelatedOnlyFieldListFilter),
        "position_type",
        "position_val",
        PlayerObjectContainedListFilter,
        "enchant",
        "min_level",
        "object__flag__artifact",
        "object__flag__relic"
    )
    readonly_fields = (
        "player_objects_id","player", "object", "parent_player_object",
        "position_type", "position_val",
        "is_contained", "enchant", "timer", "state", "bound", "min_level",
        "val0", "val1", "val2", "val3"
    )
    search_fields = (
        "player__name", "object__vnum", "object__name", "object__longname"
    )
    show_facets = admin.ShowFacets.ALWAYS
    show_full_result_count = True

    @admin.display(
        description="Contained?", boolean=True, ordering="parent_player_object"
    )
    def is_contained(self, obj) -> bool:
        return obj.is_contained()

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return self.has_add_permission(request, obj)

    def has_delete_permission(self, request, obj=None) -> bool:
        return self.has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)
