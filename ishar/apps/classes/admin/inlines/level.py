from django.contrib.admin import TabularInline

from ...models.level import ClassLevel


class ClassLevelTabularInline(TabularInline):
    """
    Class Levels tabular inline administration.
    """
    extra = 1
    fields = ("level", "male_title", "female_title", "experience")
    model = ClassLevel
