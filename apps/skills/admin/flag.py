from django.contrib.admin import ModelAdmin, register

from ..models.flag import SpellFlag


@register(SpellFlag)
class SpellFlagAdmin(ModelAdmin):
    """Spell flag administration."""

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "name",
                    "description"
                )
            }
        ),
    )
    list_display = search_fields = ("name", "description")
    model = SpellFlag
    readonly_fields = ("id",)
    verbose_name = "Flag"
    verbose_name_plural = "Flags"

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
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

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False
