from django.contrib.admin import TabularInline

from apps.skills.models.spell_flag import SkillSpellFlag


class SkillSpellFlagAdminInline(TabularInline):
    """Skill/spell flag inline administration."""
    extra = 1
    model = SkillSpellFlag
    verbose_name = "Flag"
    verbose_name_plural = "Flags"

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
