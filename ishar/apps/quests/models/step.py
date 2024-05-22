from django.db import models

from .quest import Quest
from .type.step import QuestStepType


class QuestStep(models.Model):
    """Ishar quest step."""
    step_id = models.AutoField(
        primary_key=True,
        help_text="Quest step identification number",
        verbose_name="Quest Step ID"
    )
    step_type = models.IntegerField(
        choices=QuestStepType,
        help_text="Quest step type.",
        verbose_name="Step Type",
    )
    target = models.IntegerField(
        help_text="Target of the quest step.",
        verbose_name="Target"
    )
    num_required = models.IntegerField(
        help_text="Number required for the quest step.",
        verbose_name="Number Required"
    )
    quest = models.ForeignKey(
        null=False,
        to=Quest,
        on_delete=models.DO_NOTHING,
        related_name='steps',
        related_query_name='step',
        help_text="Quest related to the quest step.",
        verbose_name="Quest"
    )
    time_limit = models.IntegerField(
        help_text="Time limit for the quest step.",
        verbose_name="Time Limit"
    )
    mystify = models.BooleanField(
        help_text="Mystify Quest Step.",
        verbose_name="Mystify"
    )
    mystify_text = models.CharField(
        blank=True,
        max_length=80,
        help_text="Mystify text for the quest step.",
        verbose_name="Mystify Text"
    )
    auto_complete = models.BooleanField(
        blank=True,
        default=False,
        null=True,
        help_text="Boolean whether the quest step is automatically completed."
    )

    class Meta:
        managed = False
        db_table = "quest_steps"
        default_related_name = "step"
        ordering = ("step_id",)
        verbose_name = "Step"
        verbose_name_plural = "Steps"

    def __repr__(self) -> str:
        return "%s %s (%d)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self) -> str:
        return "%s %d (%d) @ %s" % (
            self.get_step_type_display(),
            self.target,
            self.num_required,
            self.quest
        )
