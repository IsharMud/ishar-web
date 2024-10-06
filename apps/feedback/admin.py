from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import FeedbackSubmission, FeedbackSubmissionType



class FeedbackCompleteListFilter(admin.SimpleListFilter):
    """Admin list filter to identify (in)complete feedback submissions."""

    title = "Completed?"
    parameter_name = "completed"

    def lookups(self, request, model_admin):
        return (
            ("1", _("Yes")),
            ("0", _("No"))
        )

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == "1":
                queryset = queryset.filter(
                    submission_type__exact=FeedbackSubmissionType.COMPLETE
                )
            if self.value() == "0":
                queryset = queryset.exclude(
                    submission_type__exact=FeedbackSubmissionType.COMPLETE
                )
        return queryset


@admin.register(FeedbackSubmission)
class FeedbackAdmin(admin.ModelAdmin):
    """Ishar feedback administration."""

    actions = ("mark_complete",)
    actions_on_bottom = actions_on_top = True
    date_hierarchy = "submitted"
    fields = (
        "submission_id", "submission_type", "is_complete", "account",
        "submitted", "subject", "body_text"
    )
    list_display = (
        "submission_id", "subject", "submission_type", "is_complete",
        "account", "submitted"
    )
    list_display_links = ("submission_id", "subject")
    list_filter = (
        "submission_type",
        ("account", admin.RelatedOnlyFieldListFilter),
        "submitted",
        FeedbackCompleteListFilter
    )
    readonly_fields = (
        "submission_id", "subject", "body_text", "account", "submitted",
        "is_complete"
    )
    search_fields = ("subject", "body_text", "account__account_name")
    show_facets = admin.ShowFacets.ALWAYS
    show_full_result_count = True
    verbose_name = "Submission"
    verbose_name_plural = "Submissions"

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
        if request.user and not request.user.is_anonymous:
            if request.user.is_god():
                return True
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)

    @admin.display(description="Complete?", ordering="-submission_type")
    def is_complete(self, obj):
        return obj.is_complete()
    is_complete.boolean = True

    @admin.action(description=f"Mark selected {verbose_name_plural} complete")
    def mark_complete(self, request, queryset):
        for obj in queryset:
            obj_url = reverse(
                viewname="admin:feedback_feedbacksubmission_change",
                args=(obj.pk,)
            )
            if obj.mark_complete():
                level = messages.SUCCESS
                message_prep = _("Successfully marked")
            else:
                level = messages.ERROR
                message_prep = _("Failed to mark")
            messages.add_message(
                request=request,
                level=level,
                message=format_html(
                    '{} {} <a href="{}">{} ({})</a> as complete.',
                    message_prep,
                    self.verbose_name,
                    obj_url,
                    obj.subject,
                    obj.pk
                )
            )
        return redirect(
            reverse(viewname="admin:feedback_feedbacksubmission_changelist")
        )
