from django.contrib import admin
from ..models.vote import FeedbackVote


@admin.register(FeedbackVote)
class FeedbackVoteAdmin(admin.ModelAdmin):
    """Ishar feedback administration."""

    actions_on_bottom = actions_on_top = True
    date_hierarchy = "voted"
    fields = list_display = readonly_fields = (
        "voted",
        "feedback_submission",
        "vote_value",
        "account",
    )
    list_filter = (
        "vote_value",
        "feedback_submission",
        ("account", admin.RelatedOnlyFieldListFilter),
        "voted",
    )
    search_fields = (
        "feedback_submission__subject",
        "account__account_name"
    )
    show_facets = admin.ShowFacets.ALWAYS
    show_full_result_count = True
    verbose_name = "Vote"
    verbose_name_plural = "Votes"

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            if request.user.is_forger():
                return True
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj)
