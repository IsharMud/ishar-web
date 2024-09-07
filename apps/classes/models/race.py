from django.db import models

from apps.classes.models import Class

from apps.races.models.race import Race


class ClassRace(models.Model):
    """Ishar class race."""
    classes_races_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated, primary key for class race identifier.",
        verbose_name="Class Race ID"
    )
    race = models.ForeignKey(
        to=Race,
        db_column="race_id",
        on_delete=models.DO_NOTHING,
        help_text="Race of the class race relation.",
        verbose_name="Race"
    )
    player_class = models.ForeignKey(
        to=Class,
        db_column="class_id",
        on_delete=models.DO_NOTHING,
        help_text="Class of the class race relation.",
        verbose_name="Class"
    )

    class Meta:
        managed = False
        db_table = "classes_races"
        ordering = ("-classes_races_id",)
        verbose_name = "Class Race"
        verbose_name_plural = "Classes Races"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self) -> str:
        return "%s @ %s" % (
            self.race,
            self.player_class
        )
