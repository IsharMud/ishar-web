from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from ..models.choices import FeedbackSubmissionType
from ..models.submission import FeedbackSubmission

from .inlines.vote import FeedbackVoteAdminInline


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
        "submission_id", "submission_type", "vote_count", "private",
        "account", "submitted", "subject", "body_text"
    )
    inlines = (FeedbackVoteAdminInline,)
    list_display = (
        "__str__", "submission_type", "vote_count",
        "is_complete", "is_private", "account", "submitted"
    )
    list_filter = (
        "submission_type",
        "private",
        FeedbackCompleteListFilter,
        ("account", admin.RelatedOnlyFieldListFilter),
        "submitted"
    )
    readonly_fields = (
        "submission_id", "account", "submitted", "is_complete", "is_private",
        "vote_count"
    )
    search_fields = ("subject", "body_text", "account__account_name")
    show_facets = admin.ShowFacets.ALWAYS
    show_full_result_count = True
    verbose_name = "Submission"
    verbose_name_plural = "Submissions"

    @admin.display(description="Votes", ordering="votes")
    def vote_count(self, obj=None):
        return obj.get_vote_display()

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj=obj)
        if request.user and not request.user.is_anonymous:
            if not request.user.is_god():
                fields = fields + (
                    "submission_type", "subject", "body_text", "private"
                )
        return fields

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
    def is_complete(self, obj) -> bool:
        return obj.is_complete()
    is_complete.boolean = True

    @admin.display(description="Private?", ordering="-private")
    def is_private(self, obj) -> bool:
        return obj.is_private()
    is_private.boolean = True

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
