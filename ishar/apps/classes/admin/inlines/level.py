from django.contrib.admin import TabularInline

from ishar.apps.classes.models.level import ClassLevel


class ClassLevelInlineAdmin(TabularInline):
    """
    Class Levels tabular inline administration.
    """
    extra = 1
    fields = ("level", "male_title", "female_title", "experience")
    model = ClassLevel
