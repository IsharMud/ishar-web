from django.contrib import admin

from ..models.upgrade import AccountUpgrade


@admin.register(AccountUpgrade)
class AccountUpgradeAdmin(admin.ModelAdmin):
    """
    Ishar account upgrade administration.
    """
    fieldsets = (
        (None, {"fields": ("id", "name", "description", "is_disabled")}),
        ("Values", {"fields": (
            "amount", "cost", "increment", "max_value", "scale"
        )})
    )
    filter_horizontal = filter_vertical = ()
    list_display = ("name", "is_disabled", "description")
    list_filter = ("is_disabled",)
    search_fields = ("name", "description")
    readonly_fields = ("id",)
