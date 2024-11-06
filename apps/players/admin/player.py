from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .inlines.common import PlayerCommonInlineAdmin
from .inlines.flag import PlayerFlagsInlineAdmin
from .inlines.object import PlayerObjectsInlineAdmin
from .inlines.stat import PlayerStatInlineAdmin
from .inlines.upgrade import PlayerRemortUpgradesInlineAdmin


class PlayerAdmin(admin.ModelAdmin):
    """Ishar player administration."""

    date_hierarchy = "birth"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "account",
                    "name",
                    "description",
                    "true_level",
                    "game_type",
                    "deaths",
                    "is_deleted",
                )
            },
        ),
        (
            "Points",
            {
                "fields": (
                    "bankacc",
                    "renown",
                    "remorts",
                    "favors",
                    "seasonal_earned",
                )
            }
        ),
        (
            "Totals",
            {
                "fields": (
                    "total_renown",
                    "quests_completed",
                    "challenges_completed"
                )
            },
        ),
        (
            "Rooms",
            {
                "fields": (
                    "bound_room",
                    "load_room",
                    "inn_limit"
                )
            }
        ),
        (
            "Time",
            {
                "fields": (
                    "birth",
                    "logon",
                    "logout",
                    "online",
                    "online_timedelta",
                    "online_time",
                )
            },
        ),
        (
            "Titles",
            {
                "fields": (
                    "title",
                    "title_id"
                )
            }
        ),
    )
    inlines = (
        PlayerCommonInlineAdmin,
        PlayerFlagsInlineAdmin,
        PlayerObjectsInlineAdmin,
        PlayerRemortUpgradesInlineAdmin,
        PlayerStatInlineAdmin,
    )
    list_display = (
        "name",
        "get_account_link",
        "player_type",
        "is_hardcore",
        "is_survival",
        "player_level",
        "renown",
    )
    list_filter = (
        "game_type",
        (
            "account",
            admin.RelatedOnlyFieldListFilter
        ),
    )
    readonly_fields = (
        "id",
        "birth",
        "game_type",
        "logon",
        "logout",
        "player_type",
        "player_level",
        "online_timedelta",
        "online_time",
        "seasonal_earned",
        "title",
        "title_id",
    )
    search_fields = ("name", "account__account_name")
    show_facets = admin.ShowFacets.ALWAYS
    show_full_result_count = True
    verbose_name = "Player"
    verbose_name_plural = "Players"

    @admin.display(description="Level", ordering="common__level")
    def player_level(self, obj=None):
        return obj.common.level

    @admin.display(description="Account", ordering="account")
    def get_account_link(self, obj):
        # Admin link for account display.
        return format_html(
            '<a href="{}">{}</a>',
            reverse(
                viewname="admin:accounts_account_change",
                args=(obj.account.account_id,)
            ),
            obj.account.account_name,
        )

    def has_add_permission(self, request) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_module_permission(self, request) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False
