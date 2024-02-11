from django.contrib.admin import TabularInline

from ishar.apps.classes.models import ClassLevel


class ClassLevelInlineAdmin(TabularInline):
    """
    Class Levels tabular inline administration.
    """
    classes = ("collapse",)
    extra = 1
    fields = ("level", "male_title", "female_title", "experience")
    model = ClassLevel
