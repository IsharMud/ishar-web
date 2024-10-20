from django.contrib.admin import (
    ModelAdmin, register, RelatedOnlyFieldListFilter
)

from ..models.affinity import RaceAffinity


@register(RaceAffinity)
class RaceAffinityAdmin(ModelAdmin):
    """Ishar race affinity administration."""

    model = RaceAffinity
    fieldsets = (
        (None, {"fields": ("race_affinity_id",)}),
        ("Race", {"fields": ("race",)}),
        ("Force", {"fields": ("force",)}),
        ("Affinity", {"fields": ("affinity_type",)})
    )
    list_display = list_display_links = (
        "race_affinity_id", "race", "force", "affinity_type"
    )
    list_filter = (
        "affinity_type",
        ("force", RelatedOnlyFieldListFilter),
        ("race", RelatedOnlyFieldListFilter),
    )
    readonly_fields = ("race_affinity_id",)
    search_fields = ("race", "force", "affinity_type")

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)

    def has_change_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)

    def has_delete_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)
