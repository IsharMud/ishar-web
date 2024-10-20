from django.conf import settings
from django.contrib import admin

from .player import PlayerAdmin


class ImmortalTypeListFilter(admin.SimpleListFilter):
    """Find players of certain immortal type by "__common__level"."""

    title = "Immortal Type"
    parameter_name = "immortal_type"

    def lookups(self, request, model_admin):
        return settings.IMMORTAL_LEVELS

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(common__level=self.value())
        return queryset


class ImmortalAdmin(PlayerAdmin):
    """Ishar immortal administration."""

    date_hierarchy = "birth"
    list_display = ("name", "get_account_link", "immortal_type", "player_level")
    list_filter = (
        ImmortalTypeListFilter,
        ("account", admin.RelatedOnlyFieldListFilter),
    )
    ordering = (
        "true_level",
        "common__level",
    )

    @admin.display(description="Immortal Type", ordering="player_level")
    def immortal_type(self, obj) -> str:
        return obj.get_immortal_type()

    def has_change_permission(self, request, obj=None) -> bool:
        # Disable changing immortals.
        return False
