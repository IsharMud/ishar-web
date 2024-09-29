from django.contrib import admin

from .filters import ImmortalTypeListFilter
from .player import PlayerAdmin
from ..models.immortal import Immortal


@admin.register(Immortal)
class ImmortalAdmin(PlayerAdmin):
    """Ishar immortal administration."""
    date_hierarchy = "birth"
    list_display = (
        "name", "get_account_link", "immortal_type", "player_level"
    )
    list_filter = (
        ImmortalTypeListFilter,
        ("account", admin.RelatedOnlyFieldListFilter),
    )
    model = Immortal
    ordering = ("true_level", "common__level",)
    @admin.display(description="Immortal Type", ordering="player_level")
    def immortal_type(self, obj) -> str:
        return obj.get_immortal_type()

    def has_change_permission(self, request, obj=None) -> bool:
        """Disable changing immortals."""
        return False
