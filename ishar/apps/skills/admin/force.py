from django.contrib.admin import ModelAdmin, register

from ishar.apps.skills.models.force import Force


@register(Force)
class ForceAdmin(ModelAdmin):
    """
    Force administration.
    """
    fields = ("id", "force_name")
    list_display = list_display_links = search_fields = fields
    readonly_fields = ("id",)

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False
