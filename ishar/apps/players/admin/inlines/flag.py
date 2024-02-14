from django.contrib.admin import display, TabularInline
from django.urls import reverse
from django.utils.html import format_html

from ishar.apps.players.models.flag import PlayersFlag


class PlayerFlagsInlineAdmin(TabularInline):
    """
    Player's flags tabular inline administration.
    """
    model = PlayersFlag
    classes = ("collapse",)
    fields = readonly_fields = ("get_flag_link", "value")
    ordering = ("-value", "flag__name")
    verbose_name = "Flag"
    verbose_name_plural = "Flags"

    def get_queryset(self, request):
        return super().get_queryset(request).filter(value__gt=0)

    @display(description="Player Flag", ordering="flag__name")
    def get_flag_link(self, obj) -> str:
        """Admin link for player flag."""
        return format_html(
            '<a href="%s">%s</a>' % (
                reverse(
                    viewname="admin:players_playerflag_change",
                    args=(obj.flag.flag_id,)
                ),
                obj.flag.name
            )
        )

    def has_add_permission(self, request, obj=None) -> bool:
        """Disable adding player's flags inline."""
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        """Disable changing player's flags inline."""
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        """Disable deleting player's flags inline."""
        return False
