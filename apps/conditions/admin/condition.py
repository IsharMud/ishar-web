from django.contrib import admin

from ..models.condition import Condition


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    """Condition administration."""

    model = Condition
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "condition_id",
                    "name",
                )
            }
        ),
    )
    list_display = ("name",)
    list_filter = ("name",)
    readonly_fields = ("condition_id",)
    search_fields = ("name",)

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)

    def has_change_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)

    def has_delete_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)
