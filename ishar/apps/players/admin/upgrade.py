from django.contrib.admin import ModelAdmin, register

from ishar.apps.players.models.remort_upgrade import RemortUpgrade


@register(RemortUpgrade)
class RemortUpgradeAdmin(ModelAdmin):
    """
    Remort upgrades administration.
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
    list_display = ("display_name", "can_buy", "bonus")
    list_filter = (
        "can_buy", "bonus", "max_value",
        "renown_cost", "survival_renown_cost", "scale", "survival_scale"
    )
    readonly_fields = ("upgrade_id",)
    search_fields = ("name", "display_name")
    verbose_name = "Remort Upgrade"
    verbose_name_plural = "Remort Upgrades"
