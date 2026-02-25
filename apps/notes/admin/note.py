from django.contrib.admin import display, ModelAdmin


class NoteAdmin(ModelAdmin):
    """Admin note administration."""

    fields = ("name", "category", "body", "note_file",)
    list_display = ("name", "category",)
    list_filter = ("category",)
    list_select_related = ("category",)
    readonly_fields = ("note_id",)
    search_fields = ("name", "body", "note_file",)

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            if request.user.is_forger():
                return True
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            if request.user.is_forger():
                return True
        return False

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False
