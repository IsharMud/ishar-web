from django.contrib.admin import TabularInline

from ...models.race import ClassRace


class ClassRaceTabularInline(TabularInline):
    """
    Class Race tabular inline administration.
    """
    extra = 1
    fields = ("race", "player_class")
    model = ClassRace
