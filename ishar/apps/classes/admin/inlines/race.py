from django.contrib.admin import TabularInline

from ishar.apps.classes.models.race import ClassRace


class ClassRaceInlineAdmin(TabularInline):
    """
    Class Race tabular inline administration.
    """
    classes = ("collapse",)
    extra = 1
    fields = ("race", "player_class")
    model = ClassRace
