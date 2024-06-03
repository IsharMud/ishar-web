from django.contrib.admin import register

from .player import PlayerAdmin
from ..models.immortal import Immortal


@register(Immortal)
class ImmortalAdmin(PlayerAdmin):
    """Ishar immortal administration."""
    date_hierarchy = "birth"
    list_display = ("name", "get_account_link", "player_type", "player_level")
    model = Immortal

    def has_change_permission(self, request, obj=None) -> bool:
        """Disable changing immortals."""
        return False
