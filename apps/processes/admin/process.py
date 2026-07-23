from django.contrib.admin import action, ModelAdmin, register
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.utils.translation import gettext_lazy as _

from ..models.process import MUDProcess
from ..utils.process import get_process


@register(MUDProcess)
class MUDProcessAdmin(ModelAdmin):
    """MUD process administration."""

    # The old "Restart" button here shelled out to `sudo systemctl restart` on
    # the host (apps/processes/utils/service.py) — a bare-metal relic that is
    # broken in the container model and was security-sensitive. It is retired in
    # favour of the Forger-gated web deploy page (portal:deploy, #1754). The
    # terminate/kill signal actions remain but only see this container's process
    # table; the game runs in a separate container, so they are largely inert in
    # prod too (tracked as follow-up cleanup, out of scope for #1754).

    model = MUDProcess
    actions = (
        "terminate",
        "kill",
    )
    list_display = ("process_id", "name", "user", "runtime")
    fields = readonly_fields = list_display + (
        "created",
        "last_updated",
    )
    verbose_name = "MUD Process"
    verbose_name_plural = "MUD Processes"

    def get_changelist(self, request, **kwargs):
        get_process()
        if self.model.objects.count() == 0:
            messages.warning(
                request=request,
                message=_("No MUD process found!")
            )
        return super().get_changelist(request, **kwargs)

    def has_add_permission(self, request) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request)

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_module_permission(self, request) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request)

    @action(description="Kill")
    def kill(self, request, queryset):
        for obj in queryset:
            if obj.kill():
                level = messages.SUCCESS
                message = "Successfully sent SIGKILL to process ID %d."
            else:
                level = messages.ERROR
                message = "Failed sending SIGKILL to process ID %d."
            messages.add_message(
                request=request,
                level=level,
                message=_(message % (obj.process_id,))
            )
        return redirect(
            reverse("admin:processes_mudprocess_changelist")
        )

    @action(description="Terminate")
    def terminate(self, request, queryset):
        for obj in queryset:
            if obj.terminate():
                level = messages.SUCCESS
                message = "Successfully sent SIGTERM to process ID %d."
            else:
                level = messages.ERROR
                message = "Failed sending SIGTERM to process ID %d."
            messages.add_message(
                request=request,
                level=level,
                message=_(message % (obj.process_id,))
            )
        return redirect(
            reverse("admin:processes_mudprocess_changelist")
        )
