from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Player, RemortUpgrade


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
            qs = qs.filter(true_level=self.value())
        return qs


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """
    Ishar player administration.
    """

    date_hierarchy = "birth"
    fieldsets = (
        (None, {"fields": (
            "id", "player_type", "account", "name", "description",
            "true_level", "game_type", "is_deleted", "online"
        )}),
        ("Points", {"fields": ("bankacc", "renown", "remorts", "favors")}),
        ("Totals", {"fields": (
            "deaths", "total_renown", "quests_completed", "challenges_completed"
        )}),
        ("Rooms", {"fields": ("bound_room", "load_room", "inn_limit")}),
        ("Dates", {"fields": ("birth", "logon", "logout")})
    )
    list_display = (
        "name", "get_account_link", "player_type", "is_survival", "is_deleted",
        "level", "renown"
    )
    list_filter = (
        "game_type", "is_deleted", ImmortalTypeListFilter,
        ("account", admin.RelatedOnlyFieldListFilter), "true_level",
    )
    readonly_fields = ("id", "birth", "logon", "logout", "player_type")
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

    def get_account_link(self, obj):
        """
        Admin link for account display.
        """
        account_id = obj.account.account_id
        account_name = obj.account.account_name
        return mark_safe(
            f'<a href="/admin/accounts/account/{account_id}">{account_name}</a>'
        )
    get_account_link.short_description = "Account"
    get_account_link.admin_order_field = "account"


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
    filter_horizontal = filter_vertical = ()
    list_display = ("display_name", "can_buy", "bonus")
    list_filter = ("can_buy", "bonus")
    readonly_fields = ("upgrade_id",)
    search_fields = ("name", "display_name")
