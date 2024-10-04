from django.contrib.admin import TabularInline

from apps.skills.models.skill_force import SkillForce


class SkillForceAdminInline(TabularInline):
    """Skill force inline administration."""
    extra = 1
    model = SkillForce
    verbose_name = "Force"
    verbose_name_plural = "Forces"

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
