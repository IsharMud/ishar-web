from django.contrib.admin import ModelAdmin, register
from django.contrib import messages

from ..models.server import MUDProcess, get_process


@register(MUDProcess)
class MUDProcessAdmin(ModelAdmin):
    """MUD process administration."""
    model = MUDProcess
    fields = list_display = readonly_fields = (
        "process_id", "name", "user", "last_updated"
    )
    verbose_name = "MUD Process"
    verbose_name_plural = "MUD Processes"

    def get_model_perms(self, request):
        try:
            get_process()
        except PermissionError:
            pass
            messages.error(
                request= request,
                message=(
                    "Sorry, but there is no permission to find the process ID."
                )
            )
        return super().get_model_perms(request)

    def has_add_permission(self, request) -> bool:
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
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False
