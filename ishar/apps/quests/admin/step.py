from django.contrib import admin

from ..models.step import QuestStep


@admin.register(QuestStep)
class QuestStepsAdmin(admin.ModelAdmin):
    """
    Ishar quest step administration.
    """
    fieldsets = (
        (None, {"fields": ("step_id", "step_type", "quest")}),
        ("Details", {"fields": ("target", "num_required", "time_limit")}),
        ("Mystify", {"fields": ("mystify", "mystify_text")})
    )
    filter_horizontal = filter_vertical = ()
    list_display = ("step_id", "step_type", "quest", "mystify")
    list_filter = (
        "step_type", "num_required", "mystify",
        "quest__class_restrict", ("quest", admin.RelatedOnlyFieldListFilter),
    )
    model = QuestStep
    readonly_fields = ("step_id",)
    search_fields = (
        "step_id", "step_type", "target", "mystify_text",
        "quest__name", "quest__display_name", "quest__class_restrict"
    )

    def has_add_permission(self, request, obj=None):
        return request.user.is_immortal()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_immortal()

    def has_view_or_change_permission(self, request, obj=None):
        return request.user.is_immortal()


class QuestStepsAdminInline(admin.TabularInline):
    """
    Ishar quest step administration inline.
    """
    extra = 1
    model = QuestStep

    def has_add_permission(self, request, obj=None):
        return request.user.is_immortal()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_immortal()

    def has_view_or_change_permission(self, request, obj=None):
        return request.user.is_immortal()
