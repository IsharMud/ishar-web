from django.contrib.admin import ModelAdmin


class AccountFatedSkillAdmin(ModelAdmin):
    """Read-only view of bound threads; the game is the only writer."""

    list_display = ("account_fated_id", "account", "skill", "skill_level", "is_severed")
    list_display_links = ("account_fated_id",)
    list_select_related = ("account", "skill")
    readonly_fields = ["account_fated_id", "account", "skill", "skill_level"]
    search_fields = ("account__account_name", "skill__skill_name")

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False
