from django.contrib.admin import display, TabularInline
from django.urls import reverse
from django.utils.html import format_html

from ishar.apps.players.models.player import Player


class AccountPlayersLinksAdmin(TabularInline):
    """
    Account players links tabular inline administration.
    """
    model = Player
    verbose_name = "Player"
    verbose_name_plural = "Players"

    @display(description="Class")
    def get_player_class(self, obj) -> str:
        """Admin text for player class."""
        return obj.common.player_class.get_class_name()

    @display(boolean=True, description="Deleted?", ordering="is_deleted")
    def get_player_deleted(self, obj) -> bool:
        """Admin boolean for whether player is deleted."""
        if obj.is_deleted > 0:
            return True
        return False

    @display(description="Level")
    def get_player_level(self, obj) -> int:
        """Admin text for player level."""
        return obj.common.level

    @display(description="Player", ordering="name")
    def get_player_link(self, obj) -> str:
        """Admin link for player name."""
        return format_html(
            '<a href="%s">%s</a>' % (
                reverse(
                    viewname="admin:players_player_change",
                    args=(obj.id,)
                ),
                obj.name
            )
        )

    @display(description="Game Type", ordering="game_type")
    def get_player_game_type(self, obj) -> str:
        """Admin text for player game type."""
        return obj.get_game_type_display()

    @display(description="Race")
    def get_player_race(self, obj) -> str:
        """Admin text for player race."""
        return obj.common.race

    fields = readonly_fields = (
        "get_player_link", "get_player_class", "get_player_race",
        "get_player_level", "get_player_game_type", "get_player_deleted"
    )

    def has_add_permission(self, request, obj) -> bool:
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
