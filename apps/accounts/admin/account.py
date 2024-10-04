from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .inlines.player import AccountPlayersLinksAdmin
from .inlines.soulbound_item import AccountSoulboundItemAdmin
from .inlines.title import AccountTitleAdmin
from .inlines.upgrade import AccountUpgradesLinksAdmin


class AccountAdmin(UserAdmin):
    """Account administration."""
    model = get_user_model()
    date_hierarchy = "created_at"
    fieldsets = (
        (None, {"fields": (
            "account_id", model.USERNAME_FIELD, model.EMAIL_FIELD,
            "immortal_level", "free_refresh"
        )}),
        ("Points", {"fields": (
            "achievement_points", "current_essence", "earned_essence",
            "bugs_reported"
        )}),
        ("Last", {"fields": ("last_ident", "last_ip", "last_isp")}),
        ("Created", {"fields": ("create_ident", "create_ip", "create_isp")}),
        ("Dates", {"fields": ("account_gift", "banned_until", "created_at")})
    )
    filter_horizontal = ()
    list_filter = ("immortal_level",)
    inlines = (
        AccountPlayersLinksAdmin, AccountSoulboundItemAdmin,
        AccountTitleAdmin, AccountUpgradesLinksAdmin
    )
    list_display = (
        model.USERNAME_FIELD, model.EMAIL_FIELD, "player_count",
        "current_essence", "immortal_level"
    )
    ordering = ("account_id",)
    readonly_fields = (
        "account_id", "created_at", "player_count", "create_ip", "create_isp",
        "create_ident", "last_ip", "last_isp", "last_ident"
    )
    search_fields = (model.USERNAME_FIELD, model.EMAIL_FIELD)

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
        return self.has_module_permission(request)
