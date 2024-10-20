from django.contrib.admin import TabularInline

from apps.skills.models.component import SkillComponent


class SkillComponentAdminInline(TabularInline):
    """Skill/spell components inline administration."""

    extra = 1
    model = SkillComponent
    verbose_name = "Component"
    verbose_name_plural = "Components"

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_eternal()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_forger()
        return False
