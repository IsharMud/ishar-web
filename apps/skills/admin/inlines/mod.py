from django.contrib.admin import TabularInline

from apps.skills.models.mod import SkillMod


class SkillModAdminInline(TabularInline):
    """Skill/spell mod inline administration."""

    extra = 1
    model = SkillMod
    verbose_name = "Mod"
    verbose_name_plural = "Mods"

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
