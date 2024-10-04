from django.contrib.admin import EmptyFieldListFilter, ModelAdmin, register

from ..models.affect_flag import AffectFlag


class AffectFlagAdmin(ModelAdmin):
    """Affect flag administration."""

    model = AffectFlag
    list_display = (
        "flag_id", "display_name", "name", "is_beneficial", "item_description"
    )
    list_display_links = ("flag_id", "display_name", "name")
    list_filter = ("is_beneficial", ("item_description", EmptyFieldListFilter),)
    readonly_fields = ("flag_id",)
    search_fields = ("flag_id", "display_name", "name", "item_description")
    verbose_name = "Player's Flag"
    verbose_name_plural = "Player's Flags"

    def has_add_permission(self, request) -> bool:
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
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False
