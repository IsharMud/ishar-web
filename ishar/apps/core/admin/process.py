from django.contrib.admin import ModelAdmin, register
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from ..models.process import MUDProcess
from ..util.process import get_process


@register(MUDProcess)
class MUDProcessAdmin(ModelAdmin):
    """MUD process administration."""
    model = MUDProcess
    list_display = ("process_id", "name", "user", "created", "runtime")
    fields = readonly_fields = list_display + ("last_updated", "created")
    verbose_name = "MUD Process"
    verbose_name_plural = "MUD Processes"

    def get_list_filter(self, request):
        get_process()
        if self.model.objects.count() == 0:
            messages.warning(
                request=request,
                message=_("No MUD process found!")
            )
        return super().get_list_filter(request)

    def has_add_permission(self, request) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
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
