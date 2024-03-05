from django.db import models

from ishar.apps.classes.models import Class

from .achievement import Achievement


class AchievementClassRestrict(models.Model):
    """Ishar achievement class restriction."""
    acr_id = models.AutoField(
        db_column="acr_id",
        primary_key=True,
        help_text="Achievement class restriction identification primary key.",
        verbose_name="Achievement Class Restriction ID"
    )
    achievement = models.OneToOneField(
        db_column="achievement_id",
        to=Achievement,
        to_field="achievement_id",
        on_delete=models.DO_NOTHING,
        help_text="Achievement which is restricted to a specific class.",
        verbose_name="Achievement"
    )
    player_class = models.ForeignKey(
        blank=True,
        db_column="class_id",
        null=True,
        to=Class,
        to_field="class_id",
        on_delete=models.DO_NOTHING,
        help_text="Class which the achievement is restricted to.",
        verbose_name="Class"
    )

    class Meta:
        db_table = "achievement_class_restrict"
        managed = False
        ordering = ("player_class", "achievement",)
        verbose_name = "Achievement Class Restriction"
        verbose_name_plural = "Achievement Class Restrictions"

    def __repr__(self):
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self):
        return "%s @ %s" % (self.player_class, self.achievement)
