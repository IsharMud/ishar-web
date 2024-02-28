from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from ishar.apps.players.models.player import Player

from .filters import ImmortalTypeListFilter
from .inlines.common import PlayerCommonInlineAdmin
from .inlines.flag import PlayerFlagsInlineAdmin
from .inlines.upgrade import PlayerRemortUpgradesInlineAdmin


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """
    Player administration.
    """
    date_hierarchy = "birth"
    fieldsets = (
        (None, {"fields": (
            "id", "account", "name", "description", "true_level", "deaths"
        )}),
        ("Points", {"fields": ("bankacc", "renown", "remorts", "favors")}),
        ("Survival?", {
            "fields": ("game_type",),
        }),
        ("Deleted?", {
            "fields": ("is_deleted",),
        }),
        ("Totals", {
            "fields": (
                "total_renown", "quests_completed", "challenges_completed"
            ),
        }),
        ("Rooms", {
            "fields": ("bound_room", "load_room", "inn_limit"),
        }),
        ("Time", {
            "fields": (
                "birth", "logon", "logout",
                "online", "online_timedelta", "online_time"
            ),
        })
    )
    inlines = (
        PlayerCommonInlineAdmin,
        PlayerFlagsInlineAdmin,
        PlayerRemortUpgradesInlineAdmin
    )
    list_display = (
        "name", "get_account_link", "player_type", "is_hardcore", "is_survival",
        "player_level", "renown"
    )
    list_filter = (
        "game_type", ImmortalTypeListFilter,
        ("account", admin.RelatedOnlyFieldListFilter),
    )
    readonly_fields = (
        "id", "birth", "logon", "logout", "player_type", "player_level",
        "online_timedelta", "online_time"
    )
    search_fields = ("name", "account__account_name")
    verbose_name = "Player"
    verbose_name_plural = "Players"

    def has_add_permission(self, request, obj=None) -> bool:
        """Disable adding players in /admin/."""
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        """Disable deleting players in /admin/."""
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    @admin.display(description="Level", ordering="common__level")
    def player_level(self, obj=None):
        return obj.common.level

    @admin.display(description="Account", ordering="account")
    def get_account_link(self, obj):
        """Admin link for account display."""
        return mark_safe(
            '<a href="%s">%s</a>' % (
                reverse(
                    viewname="admin:accounts_account_change",
                    args=(obj.account.account_id,)
                ),
                obj.account.account_name
            )
        )
