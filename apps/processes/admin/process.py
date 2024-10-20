from django.contrib.admin import action, ModelAdmin, register
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.urls import path
from django.utils.translation import gettext_lazy as _

from ..models.process import MUDProcess
from ..utils.process import get_process
from ..utils.service import restart_service


@register(MUDProcess)
class MUDProcessAdmin(ModelAdmin):
    """MUD process administration."""

    model = MUDProcess
    actions = (
        "terminate",
        "kill",
    )
    change_list_template = "change_list.html"
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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [path("restart/", self.restart, name="restart"),]
        return custom_urls + urls

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

    def restart(self, request,):
        if restart_service():
            messages.success(
                request=request,
                message="Successfully sent systemctl restart."
            )
        else:
            messages.error(
                request=request,
                message="Failed sending systemctl restart."
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
