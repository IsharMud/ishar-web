from django.contrib.admin import ModelAdmin


class TensionModifierAdmin(ModelAdmin):
    """Read-only view of the knot menu; the game seeds and audits it."""

    list_display = ("modifier_id", "name", "family", "tier", "weight_display", "description")
    list_display_links = ("name",)
    list_filter = ("family",)
    readonly_fields = [
        "modifier_id", "effect_key", "family", "tier", "magnitude", "weight",
        "name", "description", "secondary_effect_key", "secondary_magnitude",
    ]
    search_fields = ("name", "description", "effect_key", "family")

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False
