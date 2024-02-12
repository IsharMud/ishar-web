from django.db import models

from ishar.apps.skills.models.skill import Skill

from . import Class


class ClassSkill(models.Model):
    """
    Class Skill.
    """
    class_skills_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated primary key for class skill identifier.",
        verbose_name="Class Skill ID"
    )
    player_class = models.ForeignKey(
        to=Class,
        db_column="class_id",
        on_delete=models.DO_NOTHING,
        help_text="Class of the class skill.",
        verbose_name="Class"
    )
    skill = models.ForeignKey(
        to=Skill,
        db_column="skill_id",
        on_delete=models.DO_NOTHING,
        help_text="Skill of the class skill.",
        verbose_name="Skill"
    )
    min_level = models.IntegerField(
        db_column="min_level",
        help_text="Minimum level of the class skill.",
        verbose_name="Minimum Level"
    )
    max_learn = models.IntegerField(
        db_column="max_learn",
        help_text="Maximum learn of the class skill.",
        verbose_name="Maximum Learn"
    )

    class Meta:
        managed = False
        db_table = "class_skills"
        ordering = ("-class_skills_id",)
        verbose_name = "Class Skill"
        verbose_name_plural = "Class Skills"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__, repr(self.__str__()), self.pk
        )

    def __str__(self) -> str:
        return "%s @ %s" % (self.skill, self.player_class)
