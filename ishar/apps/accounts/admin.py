from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count
from django.utils.safestring import mark_safe

from ishar.apps.players.models import Player

from ishar.apps.accounts.models.upgrade import AccountUpgrade


class AccountPlayersLinksInline(admin.TabularInline):
    """
    Account players links tabular inline administration.
    """
    model = Player

    @admin.display(description="Class")
    def get_player_class(self, obj) -> str:
        """Admin text for player class."""
        return obj.common.player_class.get_class_name()

    @admin.display(boolean=True, description="Deleted?")
    def get_player_deleted(self, obj) -> bool:
        """Admin boolean for whether player is deleted."""
        return obj.is_deleted

    @admin.display(description="Level")
    def get_player_level(self, obj) -> int:
        """Admin text for player level."""
        return obj.common.level

    @admin.display(description="Player", ordering="name")
    def get_player_link(self, obj) -> str:
        """Admin link for player name."""
        player_id = obj.id
        player_name = obj.name
        return mark_safe(
            # TODO: url/reverse ()? this
            f'<a href="/admin/players/player/{player_id}/">{player_name}</a>'
        )

    @admin.display(description="Game Type", ordering="game_type")
    def get_player_game_type(self, obj) -> str:
        """Admin text for player game type."""
        return obj.get_game_type_display()

    @admin.display(description="Race")
    def get_player_race(self, obj) -> str:
        """Admin text for player race."""
        return obj.common.race

    fields = readonly_fields = (
        "id", "get_player_link", "get_player_class", "get_player_race",
        "get_player_level", "get_player_game_type", "get_player_deleted"
    )

    def has_add_permission(self, request, obj=None) -> bool:
        """Disabling adding players in /admin/accounts/ inline."""
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        """Disabling changing players in /admin/accounts/ inline."""
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        """Disabling deleting players in /admin/accounts/ inline."""
        return False

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False


@admin.register(get_user_model())
class AccountsAdmin(UserAdmin):
    """
    Ishar account administration.
    """
    model = get_user_model()

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            player_count=Count("player")
        ).order_by("player_count")

    @admin.display(ordering="player_count")
    def player_count(self, obj) -> int:
        return obj.player_count

    date_hierarchy = "created_at"
    fieldsets = (
        (
            None, {
                "fields": ("account_id", "account_name", model.EMAIL_FIELD)
            }
        ),
        (
            "Points", {
                "fields": ("current_essence", "earned_essence", "bugs_reported")
            }
        ),
        (
            "Last", {
                "classes": ("collapse",),
                "fields": ("last_ident", "last_isp", "_last_haddr")
            }
        ),
        (
            "Created", {
                "classes": ("collapse",),
                "fields": ("create_ident", "create_isp", "_create_haddr")
            }
        ),
        (
            "Dates", {
                "classes": ("collapse",),
                "fields": ("account_gift", "banned_until", "created_at")
            }
        )
    )
    filter_horizontal = list_filter = ()
    inlines = (AccountPlayersLinksInline,)
    list_display = (
        "account_name", model.EMAIL_FIELD, "player_count", "current_essence",
        "is_god", "is_eternal", "is_immortal"
    )
    ordering = ("account_id",)
    search_fields = (
        "account_name", model.EMAIL_FIELD,
        "create_isp", "create_ident", "last_ident", "last_isp",
        "_create_haddr", "_login_fail_haddr", "_last_haddr"
    )
    readonly_fields = (
        "account_id", "last_ident", "last_isp", "_last_haddr",
        "created_at", "create_isp", "create_ident", "_create_haddr"
    )

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        """Disabling adding players in /admin/accounts/ inline."""
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        """Disabling changing players in /admin/accounts/ inline."""
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        """Disabling deleting players in /admin/accounts/ inline."""
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False


@admin.register(AccountUpgrade)
class AccountUpgradesAdmin(admin.ModelAdmin):
    """
    Ishar account upgrade administration.
    """
    fieldsets = (
        (
            None, {
                "fields": ("id", "name", "description", "is_disabled")
            }
        ),
        (
            "Values", {
                "fields": ("amount", "cost", "increment", "max_value", "scale")
            }
        )
    )
    list_display = ("name", "is_disabled", "description")
    list_filter = ("is_disabled",)
    search_fields = ("name", "description")
    readonly_fields = ("id",)

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False
