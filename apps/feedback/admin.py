from django.contrib.admin import (
    display, ModelAdmin, register, RelatedOnlyFieldListFilter, ShowFacets
)

from .models import FeedbackSubmission


@register(FeedbackSubmission)
class FeedbackAdmin(ModelAdmin):
    """Ishar feedback administration."""

    actions_on_bottom = actions_on_top = True
    date_hierarchy = "submitted"
    fieldsets = (
        (None, {"fields": ("submission_id", "submission_type")}),
        ("Submission", {"fields": ("subject", "body_text")}),
        ("Authorship", {"fields": ("submitted", "account")})
    )
    list_display = (
        "submission_id", "submission_type", "subject", "account", "submitted"
    )
    list_display_links = ("submission_id", "submission_type", "subject")
    list_filter = (
        "submission_type", ("account", RelatedOnlyFieldListFilter), "submitted"
    )
    readonly_fields = (
        "submission_id", "subject", "body_text", "account", "submitted"
    )
    search_fields = ("subject", "body_text", "account")
    show_facets = ShowFacets.ALWAYS
    show_full_result_count = True

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            if request.user.is_forger():
                return True
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)

    def has_delete_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)
