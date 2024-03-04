from django.contrib.admin import TabularInline

from ...models.criteria import AchievementCriteria


class AchievementCriteriaTabularInline(TabularInline):
    """Achievement criteria tabular inline administration."""
    extra = 1
    model = AchievementCriteria
    verbose_name = "Criteria"
    verbose_name_plural = "Criterion"

    def has_add_permission(self, request, obj) -> bool:
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

    def has_module_permission(self, request) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False
