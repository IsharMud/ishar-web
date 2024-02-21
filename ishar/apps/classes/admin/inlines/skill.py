from django.contrib.admin import TabularInline

from ishar.apps.classes.models.skill import ClassSkill


class ClassSkillInlineAdmin(TabularInline):
    """
    Class Skill tabular inline administration.
    """
    extra = 1
    fields = ("player_class", "skill", "min_level", "max_learn")
    model = ClassSkill
