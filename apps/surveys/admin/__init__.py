"""
Survey builder administration.

Structure is authored here (survey → sections + questions inline; options on
the question page); responses are read-only — players submit via /surveys/,
and staff read results on the dashboard (/surveys/<slug>/results/).
"""
from django.contrib.admin import ModelAdmin, TabularInline, display, site

from ..models import (
    Survey,
    SurveyAnswer,
    SurveyOption,
    SurveyQuestion,
    SurveySection,
    SurveySubmission,
)


class SurveyPermsMixin:
    """Eternal+ can view; Forger+ can edit (mirrors the notes admin)."""

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False


class SurveySectionInline(SurveyPermsMixin, TabularInline):
    model = SurveySection
    extra = 0
    fields = ("position", "title", "preamble")


class SurveyQuestionInline(SurveyPermsMixin, TabularInline):
    model = SurveyQuestion
    extra = 0
    fields = (
        "section", "position", "kind", "text",
        "required", "max_choices", "allow_other",
    )
    show_change_link = True

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        section = formset.form.base_fields["section"]
        section.queryset = (
            obj.sections.all() if obj else SurveySection.objects.none()
        )
        return formset


class SurveyAdmin(SurveyPermsMixin, ModelAdmin):
    fields = (
        "title", "slug", "intro", "status", "opens_at", "closes_at",
        "created_at", "updated_at",
    )
    inlines = (SurveySectionInline, SurveyQuestionInline)
    list_display = ("title", "slug", "state", "num_submissions", "closes_at")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("title", "slug", "intro")

    @display(description="State")
    def state(self, obj) -> str:
        return obj.state_label

    @display(description="Submissions")
    def num_submissions(self, obj) -> int:
        return obj.submissions.count()


class SurveyOptionInline(SurveyPermsMixin, TabularInline):
    model = SurveyOption
    extra = 0
    fields = ("position", "text", "is_matrix_row")


class SurveyQuestionAdmin(SurveyPermsMixin, ModelAdmin):
    fields = (
        "survey", "section", "position", "kind", "text", "hint",
        "required", "max_choices", "allow_other",
    )
    inlines = (SurveyOptionInline,)
    list_display = ("text", "survey", "section", "position", "kind", "required")
    list_filter = ("survey", "kind")
    list_select_related = ("survey", "section")
    search_fields = ("text",)


class SurveyAnswerInline(SurveyPermsMixin, TabularInline):
    model = SurveyAnswer
    extra = 0
    can_delete = False
    fields = ("question", "row", "option", "rank", "text")
    readonly_fields = fields

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


class SurveySubmissionAdmin(SurveyPermsMixin, ModelAdmin):
    inlines = (SurveyAnswerInline,)
    list_display = ("submission_id", "survey", "account", "submitted_at")
    list_filter = ("survey",)
    list_select_related = ("survey", "account")
    readonly_fields = ("survey", "account", "submitted_at")

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


site.register(Survey, SurveyAdmin)
site.register(SurveyQuestion, SurveyQuestionAdmin)
site.register(SurveySubmission, SurveySubmissionAdmin)
