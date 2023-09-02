from django.contrib import admin

from ..models.remort import RemortUpgrade


@admin.register(RemortUpgrade)
class RemortUpgradeAdmin(admin.ModelAdmin):
    """
    Ishar remort upgrades administration.
    """
    model = RemortUpgrade
    fieldsets = (
        (None, {"fields": ("upgrade_id", "name", "display_name")}),
        ("Availability", {"fields": ("can_buy", "bonus", "max_value")}),
        ("Amounts", {"fields": ("renown_cost", "scale")}),
        ("Survival Amounts", {"fields": (
            "survival_renown_cost", "survival_scale")
        }),
    )
    filter_horizontal = filter_vertical = ()
    list_display = ("display_name", "can_buy", "bonus")
    list_filter = ("can_buy", "bonus")
    readonly_fields = ("upgrade_id",)
    search_fields = ("name", "display_name")
