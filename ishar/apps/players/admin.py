from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Player, PlayerCommon, PlayerFlag, RemortUpgrade


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

    def has_add_permission(self, request, obj):
        """
        Disabling adding rows to player_common.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Disabling deleting rows from player_common.
        """
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
            "fields": ("game_type", "is_deleted"),
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
            "fields": ("birth", "logon", "logout", "online", "online_time"),
            "classes": ("collapse",)
        })
    )
    inlines = (PlayerCommonInlineAdmin,)
    list_display = (
        "name", "get_account_link", "player_type", "is_survival", "is_deleted",
        "player_level", "renown"
    )
    list_filter = (
        "game_type", "is_deleted", ImmortalTypeListFilter,
        ("account", admin.RelatedOnlyFieldListFilter),
    )
    readonly_fields = (
        "id", "birth", "logon", "logout", "player_type", "player_level",
        "online_time"
    )
    search_fields = ("name", "account__account_name")

    def has_add_permission(self, request, obj=None):
        """
        Disable adding players in /admin/.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Disable deleting players in /admin/.
        """
        return False

    def has_change_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_module_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None):
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    @staticmethod
    def player_level(obj):
        return obj.common.level

    @admin.display(description="Account", ordering="account")
    def get_account_link(self, obj):
        """
        Admin link for account display.
        """
        account_id = obj.account.account_id
        account_name = obj.account.account_name
        return mark_safe(
            f'<a href="/admin/accounts/account/{account_id}">{account_name}</a>'
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
    list_filter = ("can_buy", "bonus")
    readonly_fields = ("upgrade_id",)
    search_fields = ("name", "display_name")