from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .filters import ImmortalTypeListFilter
from .inlines.common import PlayerCommonInlineAdmin
from .inlines.flag import PlayerFlagsInlineAdmin
from .inlines.stat import PlayerStatInlineAdmin
from .inlines.upgrade import PlayerRemortUpgradesInlineAdmin

from .player import PlayerAdmin
from ..models.immortal import Immortal


@admin.register(Immortal)
class ImmortalAdmin(PlayerAdmin):
    """Ishar immortal administration."""
    date_hierarchy = "birth"
    inlines = (
        PlayerCommonInlineAdmin, PlayerFlagsInlineAdmin, PlayerStatInlineAdmin
    )
    list_display = ("name", "get_account_link", "player_type", "player_level")
    list_filter = (
        ImmortalTypeListFilter, ("account", admin.RelatedOnlyFieldListFilter)
    )

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
