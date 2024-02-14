from django.contrib.admin import ModelAdmin, register

from ishar.apps.classes.models.skill import ClassSkill


@register(ClassSkill)
class ClassSkillAdmin(ModelAdmin):
    """
    Ishar class skill administration.
    """
    list_display = ("class_skills_id", "player_class", "skill")
    list_display_links = list_display
    list_filter = ("player_class", "skill", "min_level", "max_learn")
