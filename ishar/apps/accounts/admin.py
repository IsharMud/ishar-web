from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count

from .models.upgrade import AccountUpgrade
from ..players.models import Player


class AccountPlayersInlineAdmin(admin.TabularInline):
    model = Player
    fields = (
        "name", "game_type", "is_deleted", "true_level", "remorts",
        "renown", "total_renown"
    )

    def has_add_permission(self, request, obj):
        """
        Disabling adding players in /admin/accounts/ inline.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Disabling deleting players in /admin/accounts/ inline.
        """
        return False


@admin.register(get_user_model())
class AccountsAdmin(UserAdmin):
    """
    Ishar account administration.
    """
    model = get_user_model()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(player_count=Count("player")).order_by("player_count")
        return qs

    def player_count(self, obj):
        return obj.player_count
    player_count.admin_order_field = "player_count"

    date_hierarchy = "created_at"
    fieldsets = (
        (
            None, {
                "fields": (
                    "account_id", "account_name", model.EMAIL_FIELD,
                )
            }
        ),
        (
            "Points", {
                "fields": (
                    "current_essence", "earned_essence", "bugs_reported"
                )
            }
        ),
        (
            "Last", {
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
    filter_horizontal = ()
    inlines = (AccountPlayersInlineAdmin,)
    list_display = (
        "account_name", model.EMAIL_FIELD, "player_count", "current_essence",
        "is_god", "is_eternal", "is_immortal"
    )
    list_filter = ()
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

    def has_add_permission(self, request, obj=None):
        """
        Disabling adding accounts in /admin/.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Disable deleting accounts in /admin/.
        """
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_god()

    def has_module_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_view_permission(self, request, obj=None):
        return request.user.is_eternal()


@admin.register(AccountUpgrade)
class AccountUpgradesAdmin(admin.ModelAdmin):
    """
    Ishar account upgrade administration.
    """
    fieldsets = (
        (None, {"fields": ("id", "name", "description", "is_disabled")}),
        ("Values", {"fields": (
            "amount", "cost", "increment", "max_value", "scale"
        )})
    )
    list_display = ("name", "is_disabled", "description")
    list_filter = ("is_disabled",)
    search_fields = ("name", "description")
    readonly_fields = ("id",)

    def has_module_permission(self, request, obj=None):
        return request.user.is_immortal()
