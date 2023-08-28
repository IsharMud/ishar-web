from django.contrib.admin import ModelAdmin


class AccountUpgradeAdmin(ModelAdmin):
    """
    Ishar account upgrade administration.
    """
    fieldsets = (
        (None, {"fields": ("id", "name", "description", "is_disabled")}),
        ("Values", {"fields": (
            "amount", "cost", "increment", "max_value", "scale"
        )})
    )
    filter_horizontal = []
    filter_vertical = []
    list_display = ["name", "description", "_is_disabled"]
    list_filter = ["is_disabled"]
    search_fields = ["name", "description"]
    readonly_fields = ["id"]
