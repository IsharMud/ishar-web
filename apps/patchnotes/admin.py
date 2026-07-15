from django.contrib import admin

from apps.patchnotes.models import PatchNote, PatchNoteSyncTask


@admin.register(PatchNote)
class PatchNoteAdmin(admin.ModelAdmin):
    """Patch note administration (Django admin; the primary tool is the
    Patch Note editor at /patch-notes/console/)."""

    date_hierarchy = "created_at"
    fieldsets = (
        (None, {"fields": ("id",)}),
        ("Content", {"fields": ("title", "body", "season_id")}),
        ("Publishing", {"fields": ("author", "is_published", "created_at",
                                   "published_at", "discord_sent_at")}),
    )
    list_display = ("title", "author", "is_published", "season_id",
                    "created_at", "published_at")
    list_filter = ("is_published", "season_id")
    readonly_fields = ("id", "created_at", "published_at", "discord_sent_at")
    search_fields = ("title", "body", "author")

    def has_module_permission(self, request, obj=None) -> bool:
        return bool(request.user and not request.user.is_anonymous
                    and request.user.is_eternal())

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)

    def has_add_permission(self, request, obj=None) -> bool:
        return bool(request.user and not request.user.is_anonymous
                    and request.user.is_forger())

    def has_change_permission(self, request, obj=None) -> bool:
        return self.has_add_permission(request, obj)

    def has_delete_permission(self, request, obj=None) -> bool:
        return self.has_add_permission(request, obj)


@admin.register(PatchNoteSyncTask)
class PatchNoteSyncTaskAdmin(admin.ModelAdmin):
    """Read-only view of the publish outbox (audit trail)."""

    date_hierarchy = "created_at"
    list_display = ("id", "patch_note", "action", "actor", "status",
                    "attempts", "created_at", "processed_at")
    list_filter = ("status", "action")
    search_fields = ("actor", "last_error")

    def has_module_permission(self, request, obj=None) -> bool:
        return bool(request.user and not request.user.is_anonymous
                    and request.user.is_eternal())

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False
