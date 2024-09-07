from django.contrib.admin import StackedInline

from ...models.soulbound_item import AccountSoulboundItem


class AccountSoulboundItemAdmin(StackedInline):
    """
    Account soulbound item tabular inline administration.
    """
    model = AccountSoulboundItem
    extra = 1
    fields = ("item_id", "cooldown", "last_used", "time_gained", "updated_at")
    ordering = ("-last_used", "-updated_at", "item_id",)
    readonly_fields = (
        "account_soulbound_id", "last_used", "time_gained", "updated_at",
    )
    verbose_name = "Soulbound Item"
    verbose_name_plural = "Soulbound Items"

    def has_add_permission(self, request, obj) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_module_permission(self, request) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request)
