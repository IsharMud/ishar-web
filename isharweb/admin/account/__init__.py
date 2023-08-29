from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class AccountAdmin(BaseUserAdmin):
    """
    Ishar account administration.
    """

    def has_add_permission(self, request, obj=None):
        """
        Remove ability to add accounts in /admin/.
        """
        return False

    model = get_user_model()
    fieldsets = (
        (None, {"fields": [
            "account_id", model.USERNAME_FIELD, model.EMAIL_FIELD
        ]}),
        ("Points", {"fields": (
            "account_gift", "bugs_reported", "current_essence", "earned_essence"
        )}),
        ("Banned", {"fields": ("banned_until",)}),
        ("Last", {"fields": ("last_ident", "last_isp", "last_haddr")}),
        ("Created", {"fields": (
            "created_at", "create_ident", "create_isp", "create_haddr"
        )})
    )
    filter_horizontal = []
    filter_vertical = []
    inlines = []

    list_display = (
        model.USERNAME_FIELD,
        "_is_god", "_is_forger", "_is_eternal", "_is_artisan", "_is_immortal"
    )
    list_filter = []
    ordering = ["account_id"]
    search_fields = [
        model.USERNAME_FIELD, model.EMAIL_FIELD,
        "create_isp", "create_ident", "last_ident", "last_isp"
    ]
    readonly_fields = [
        "account_id", "last_ident", "last_isp", "last_haddr",
        "created_at", "create_isp", "create_ident", "create_haddr"
    ]
