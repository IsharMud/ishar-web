from django.db import models

from .skill import Skill


class SkillComponent(models.Model):
    """
    Skill Component.
    """
    skill_components_id = models.PositiveIntegerField(
        blank=False,
        db_column="skill_components_id",
        editable=False,
        null=False,
        help_text="Auto-generated ID number of the skill-component relation.",
        primary_key=True,
        verbose_name="Skill Component ID"
    )
    skill = models.ForeignKey(
        blank=False,
        db_column="skill_id",
        help_text="Skill related to a component.",
        null=False,
        on_delete=models.DO_NOTHING,
        related_name="components",
        related_query_name="component",
        to=Skill,
        verbose_name="Skill"
    )
    component_type = models.IntegerField(
        blank=False,
        choices=(
            (0, "None [0]"),
            (1, "Treasure [1]"),
            (2, "Item [2]")
        ),
        help_text="Type of component.",
        null=False,
        verbose_name="Component Type"
    )
    component_value = models.IntegerField(
        blank=False,
        help_text="Value of component.",
        null=False,
        verbose_name="Component Value"
    )
    component_count = models.SmallIntegerField(
        blank=False,
        default=1,
        null=False,
        help_text="Count of components.",
        verbose_name="Component Count"
    )

    class Meta:
        managed = False
        db_table = "skill_components"
        ordering = ("skill_components_id", "skill")
        verbose_name = "Skill Component"
        verbose_name_plural = "Skill Components"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self) -> str:
        return "%s @ %s" % (self.get_component_type_display(), self.skill)
