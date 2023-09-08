from django.contrib import admin

from ..models.upgrade import AccountUpgrade


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
    filter_horizontal = filter_vertical = ()
    list_display = ("name", "is_disabled", "description")
    list_filter = ("is_disabled",)
    search_fields = ("name", "description")
    readonly_fields = ("id",)

    def has_add_permission(self, request, obj=None):
        return request.user.is_god()

    def has_change_permission(self, request, obj=None):
        return request.user.is_god()

    def has_view_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_god()
