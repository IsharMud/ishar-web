from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, AdminPasswordChangeForm


class AccountAdmin(BaseUserAdmin):
    """
    Ishar account administration.
    """

    def has_add_permission(self, request, obj=None):
        """
        Remove ability to add users in /admin/.
        """
        return False

    change_password_form = AdminPasswordChangeForm
    fieldsets = (
        (None, {"fields": ["account_id", "account_name", "email"]}),
    )
    filter_horizontal = []
    filter_vertical = []
    list_display = [
        "account_name", "email",
        "_is_god", "_is_immortal",
    ]
    list_filter = []
    ordering = ["account_id"]
    search_fields = ["account_name", "email"]
    readonly_fields = ["account_id"]
