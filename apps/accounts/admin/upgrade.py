from django.contrib.admin import ModelAdmin


class AccountUpgradeAdmin(ModelAdmin):
    """Account upgrade administration."""

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "name",
                    "description",
                    "is_disabled"
                )
            }
        ),
        (
            "Values",
            {
                "fields": (
                    "amount",
                    "cost",
                    "increment",
                    "max_value",
                    "scale",
                    "grants_memory",
                )
            },
        ),
    )
    list_display = (
        "name",
        "is_disabled",
        "description"
    )
    list_filter = ("is_disabled",)
    search_fields = ("name", "description")
    readonly_fields = ("id",)

    def has_add_permission(self, request) -> bool:
        return self.has_module_permission(request)

    def has_change_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request)

    def has_delete_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request)

    def has_module_permission(self, request) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request)
