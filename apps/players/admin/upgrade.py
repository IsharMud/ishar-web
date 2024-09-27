from django.contrib import admin

from apps.players.models.remort_upgrade import RemortUpgrade


@admin.register(RemortUpgrade)
class RemortUpgradeAdmin(admin.ModelAdmin):
    """Remort upgrades administration."""
    model = RemortUpgrade
    fieldsets = (
        (None, {"fields": ("upgrade_id", "name", "display_name")}),
        ("Availability", {"fields": ("can_buy", "bonus", "max_value")}),
        ("Amounts", {"fields": ("renown_cost", "scale")}),
        ("Survival Amounts", {"fields": (
            "survival_renown_cost", "survival_scale"
        )}),
        ("Skill", {"fields": ("reward_skill",)}),
    )
    list_display = ("display_name", "can_buy", "bonus")
    list_filter = (
        "can_buy", "bonus", "max_value",
        "renown_cost", "survival_renown_cost", "scale", "survival_scale",
        ("reward_skill", admin.RelatedOnlyFieldListFilter)
    )
    readonly_fields = ("upgrade_id",)
    search_fields = ("name", "display_name")
    show_facets = admin.ShowFacets.ALWAYS
    verbose_name = "Remort Upgrade"
    verbose_name_plural = "Remort Upgrades"

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
