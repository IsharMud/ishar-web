from django.db import models

from . import Class


class ClassLevel(models.Model):
    """
    Ishar class level.
    """
    class_level_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated, primary key for class level identifier.",
        verbose_name="Class Level ID"
    )
    level = models.IntegerField(
        help_text="Level of the class level.",
        verbose_name="Level"
    )
    male_title = models.CharField(
        max_length=80,
        help_text="Male title of the class level.",
        verbose_name="Male Title"
    )
    female_title = models.CharField(
        max_length=80,
        help_text="Female title of the class level.",
        verbose_name="Female Title"
    )
    player_class = models.ForeignKey(
        to=Class,
        db_column="class_id",
        on_delete=models.DO_NOTHING,
        help_text="Class of the class level.",
        verbose_name="Class"
    )
    experience = models.IntegerField(
        help_text="Experience of the class level.",
        verbose_name="Experience"
    )

    class Meta:
        managed = False
        db_table = "class_levels"
        ordering = ()
        verbose_name = "Class Level"
        verbose_name_plural = "Class Levels"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__, self.__str__(), self.pk
        )

    def __str__(self) -> str:
        return "Level %i @ %s" % (self.level, self.player_class)
