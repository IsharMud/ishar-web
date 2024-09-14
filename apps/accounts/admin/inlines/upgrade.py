from django.contrib.admin import display, TabularInline
from django.urls import reverse
from django.utils.html import format_html

from ...models.upgrade import AccountAccountUpgrade


class AccountUpgradesLinksAdmin(TabularInline):
    """
    Account upgrades links tabular inline administration.
    """
    extra = 0
    model = AccountAccountUpgrade
    fields = readonly_fields = ("get_upgrade_link", "amount")
    ordering = ("-amount", "upgrade__name")
    verbose_name = "Upgrade"
    verbose_name_plural = "Upgrades"

    def get_queryset(self, request):
        return super().get_queryset(request).filter(amount__gt=0)

    @display(description="Upgrade", ordering="upgrade")
    def get_upgrade_link(self, obj) -> str:
        """Admin link for account upgrade."""
        return format_html(
            '<a href="{}">{}</a>',
            reverse(
                viewname="admin:accounts_accountupgrade_change",
                args=(obj.upgrade.id,)
            ),
            obj.upgrade.name
        )

    def has_add_permission(self, request, obj) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_module_permission(self, request) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request)
