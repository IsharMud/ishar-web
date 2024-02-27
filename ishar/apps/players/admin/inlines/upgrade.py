from django.contrib.admin import display, TabularInline
from django.urls import reverse
from django.utils.html import format_html

from ishar.apps.players.models.player_remort_upgrade import PlayerRemortUpgrade


class PlayerRemortUpgradesInlineAdmin(TabularInline):
    """
    Player's remort upgrades tabular inline administration.
    """
    model = PlayerRemortUpgrade
    fields = readonly_fields = ("get_upgrade_link", "value", "essence_perk")
    ordering = ("-value", "-essence_perk", "upgrade__display_name")
    verbose_name = "Remort Upgrade"
    verbose_name_plural = "Remort Upgrades"

    @display(description="Remort Upgrade", ordering="upgrade")
    def get_upgrade_link(self, obj) -> str:
        """Admin link for remort upgrade."""
        return format_html(
            '<a href="%s">%s</a>' % (
                reverse(
                    viewname="admin:players_remortupgrade_change",
                    args=(obj.upgrade.upgrade_id,)
                ),
                obj.upgrade.display_name
            )
        )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(value__gt=0)

    def has_add_permission(self, request, obj=None) -> bool:
        """Disable adding player's remort upgrades inline."""
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        """Disable changing player's remort upgrades inline."""
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        """Disable deleting player's remort upgrades inline."""
        return False
