from django.contrib.admin import TabularInline

from ...models.vote import FeedbackVote


class FeedbackVoteAdminInline(TabularInline):
    """Feedback submission vote inline administration."""
    extra = 0
    model = FeedbackVote
    verbose_name = "Vote"
    verbose_name_plural = "Votes"

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_add_permission(self, request, obj) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        return self.has_module_permission(request, obj=obj)
