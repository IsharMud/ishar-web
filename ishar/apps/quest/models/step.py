from django.db import models

from . import Quest


class QuestStep(models.Model):

    step_id = models.AutoField(
        primary_key=True,
        help_text="Quest step identification number",
        verbose_name="Quest Step ID"
    )
    step_type = models.IntegerField(
        choices=[(0, 'Object'), (1, 'Kill'), (2, 'Room')],
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
        on_delete=models.CASCADE,
        related_name='steps',
        related_query_name='step',
        help_text="Quest related to the quest step.",
        verbose_name="Quest"
    )
    time_limit = models.IntegerField(
        help_text="Time limit for the quest step.",
        verbose_name="Time Limit"
    )
    mystify = models.IntegerField(
        choices=[(0, False), (1, True)],
        help_text="Mystify Quest Step.",
        verbose_name="Mystify"
    )
    mystify_text = models.CharField(
        blank=True,
        max_length=80,
        help_text="Mystify text for the quest step.",
        verbose_name="Mystify Text"
    )

    class Meta:
        managed = False
        db_table = "quest_steps"
        default_related_name = "step"
        ordering = ("quest", "step_id")
        verbose_name = "Step"
        verbose_name_plural = "Steps"

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return (
            f"Quest Step: {self.step_id} ({self.get_step_type_display()}) @ "
            f"{self.quest}"
        )
