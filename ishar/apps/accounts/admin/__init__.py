from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count

from .upgrade import AccountUpgradesAdmin


@admin.register(get_user_model())
class AccountsAdmin(BaseUserAdmin):
    """
    Ishar account administration.
    """

    def has_add_permission(self, request, obj=None):
        """
        Disabling adding accounts in /admin/.
        """
        return False

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
                    "account_id", model.USERNAME_FIELD
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
    list_display = (
        model.USERNAME_FIELD, "player_count", "is_god", "is_immortal",
        "current_essence"
    )
    list_filter = ()
    ordering = ("account_id",)
    search_fields = (
        model.USERNAME_FIELD,
        "create_isp", "create_ident", "last_ident", "last_isp",
        "_create_haddr", "_login_fail_haddr", "_last_haddr"
    )
    readonly_fields = (
        "account_id", "last_ident", "last_isp", "_last_haddr",
        "created_at", "create_isp", "create_ident", "_create_haddr"
    )
