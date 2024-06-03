from django.contrib.admin import register

from .player import PlayerAdmin
from ..models.immortal import Immortal


@register(Immortal)
class ImmortalAdmin(PlayerAdmin):
    """Ishar immortal administration."""
    date_hierarchy = "birth"
    list_display = ("name", "get_account_link", "player_type", "player_level")
    model = Immortal

    def has_add_permission(self, request) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_module_permission(self, request) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request=request)
