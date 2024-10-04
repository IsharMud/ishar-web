from django.contrib.admin import TabularInline

from ...models.skill import ClassSkill


class ClassSkillTabularInline(TabularInline):
    """Class Skill tabular inline administration."""

    extra = 1
    fields = ("player_class", "skill", "min_level", "max_learn")
    model = ClassSkill
