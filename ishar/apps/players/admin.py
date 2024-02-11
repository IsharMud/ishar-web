from django.conf import settings
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from ishar.apps.players.models import Player
from ishar.apps.players.models.common import PlayerCommon
from ishar.apps.players.models.flag import PlayerFlag, PlayersFlag
from ishar.apps.players.models.upgrade import RemortUpgrade, PlayerRemortUpgrade


class ImmortalTypeListFilter(admin.SimpleListFilter):
    """
    Determine whether a player is certain type of immortal,
        based on their "true_level" column value.
    """
    title = "Immortal Type"
    parameter_name = "immortal_type"

    def lookups(self, request, model_admin):
        return settings.IMMORTAL_LEVELS

    def queryset(self, request, queryset):
        qs = queryset
        if self.value():
            qs = qs.filter(common__level=self.value())
        return qs


class PlayerCommonInlineAdmin(admin.StackedInline):
    """
    Player common inline administration.
    """
    model = PlayerCommon
    classes = ("collapse",)
    verbose_name = verbose_name_plural = "Common"

    def has_add_permission(self, request, obj=None) -> bool:
        """Disable adding rows to player_common."""
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        """Disable deleting rows from player_common."""
        return False


class PlayerFlagsInlineAdmin(admin.TabularInline):
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

    @admin.display(description="Player Flag", ordering="flag__name")
    def get_flag_link(self, obj) -> str:
        """Admin link for player flag."""
        return mark_safe(
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


class PlayerRemortUpgradesInlineAdmin(admin.TabularInline):
    """
    Player's remort upgrades tabular inline administration.
    """
    model = PlayerRemortUpgrade
    classes = ("collapse",)
    fields = readonly_fields = ("get_upgrade_link", "value", "essence_perk")
    ordering = ("-value", "-essence_perk", "upgrade__display_name")
    verbose_name = "Remort Upgrade"
    verbose_name_plural = "Remort Upgrades"

    @admin.display(description="Remort Upgrade", ordering="upgrade")
    def get_upgrade_link(self, obj) -> str:
        """Admin link for remort upgrade."""
        return mark_safe(
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


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """
    Ishar player administration.
    """
    date_hierarchy = "birth"
    fieldsets = (
        (None, {"fields": (
            "id", "account", "name", "description", "true_level", "deaths"
        )}),
        ("Points", {"fields": ("bankacc", "renown", "remorts", "favors")}),
        ("Survival?", {
            "fields": ("game_type",),
            "classes": ("collapse",)
        }),
        ("Deleted?", {
            "fields": ("is_deleted",),
            "classes": ("collapse",)
        }),
        ("Totals", {
            "fields": (
                "total_renown", "quests_completed", "challenges_completed"
            ),
            "classes": ("collapse",)
        }),
        ("Rooms", {
            "fields": ("bound_room", "load_room", "inn_limit"),
            "classes": ("collapse",)
        }),
        ("Time", {
            "fields": (
                "birth", "logon", "logout",
                "online", "online_timedelta", "online_time"
            ),
            "classes": ("collapse",)
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
            return request.user.is_god()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
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


@admin.register(PlayerFlag)
class PlayerFlagAdmin(admin.ModelAdmin):
    """
    Ishar player flag administration.
    """
    model = PlayerFlag
    fieldsets = ((None, {"fields": ("flag_id", "name")}),)
    list_display = list_display_links = search_fields = ("flag_id", "name",)
    readonly_fields = ("flag_id",)
    verbose_name = "Player's Flag"
    verbose_name_plural = "Player's Flags"


@admin.register(RemortUpgrade)
class RemortUpgradeAdmin(admin.ModelAdmin):
    """
    Ishar remort upgrades administration.
    """
    model = RemortUpgrade
    fieldsets = (
        (None, {"fields": ("upgrade_id", "name", "display_name")}),
        ("Availability", {"fields": ("can_buy", "bonus", "max_value")}),
        ("Amounts", {"fields": ("renown_cost", "scale")}),
        ("Survival Amounts", {"fields": (
            "survival_renown_cost", "survival_scale")
        }),
    )
    list_display = ("display_name", "can_buy", "bonus")
    list_filter = (
        "can_buy", "bonus", "max_value",
        "renown_cost", "survival_renown_cost", "scale", "survival_scale"
    )
    readonly_fields = ("upgrade_id",)
    search_fields = ("name", "display_name")
    verbose_name = "Remort Upgrade"
    verbose_name_plural = "Remort Upgrades"
