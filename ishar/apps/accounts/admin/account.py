from django.contrib.admin import display, register
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .inlines.player import AccountPlayersLinksAdmin
from .inlines.upgrade import AccountUpgradesLinksAdmin


@register(get_user_model())
class AccountAdmin(UserAdmin):
    """
    Account administration.
    """
    model = get_user_model()
    date_hierarchy = "created_at"
    fieldsets = (
        (
            None, {
                "fields": (
                    "account_id", model.USERNAME_FIELD, model.EMAIL_FIELD,
                    "is_private"
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
                "fields": ("last_ident", "last_ip", "last_isp")
            }
        ),
        (
            "Created", {
                "fields": ("create_ident", "create_ip", "create_isp")
            }
        ),
        (
            "Dates", {
                "fields": ("account_gift", "banned_until", "created_at")
            }
        )
    )
    filter_horizontal = ()
    inlines = (AccountPlayersLinksAdmin, AccountUpgradesLinksAdmin)
    list_display = (
        model.USERNAME_FIELD, model.EMAIL_FIELD, "player_count",
        "current_essence", "is_private"
    )
    list_filter = ()
    ordering = ("account_id",)
    search_fields = (
        model.USERNAME_FIELD, model.EMAIL_FIELD,
        "create_ip", "create_isp", "create_ident",
        "last_ip", "last_isp", "last_ident"
    )
    readonly_fields = (
        "account_id", "created_at", "player_count",
        "create_ip", "create_isp", "create_ident",
        "last_ip", "last_isp", "last_ident"
    )

    @display(description="Create IP")
    def create_ip(self, obj) -> str:
        return obj.get_create_ip()

    @display(description="Last IP")
    def last_ip(self, obj) -> str:
        return obj.get_last_ip()

    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_module_permission(self, request) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_view_or_change_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request)
