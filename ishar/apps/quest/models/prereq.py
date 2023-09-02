from django.db import models

from . import Quest


class QuestPrereq(models.Model):
    """
    Quest Prerequisite.
    """
    quest = models.ForeignKey(
        to=Quest,
        on_delete=models.CASCADE,
        help_text="Quest which requires a prerequisite.",
        verbose_name="Quest"
    )
    required_quest = models.ForeignKey(
        to=Quest,
        on_delete=models.DO_NOTHING,
        db_column="required_quest",
        help_text="Prerequisite required quest prior to another quest.",
        related_name="questprereq_required_quest_set",
        verbose_name="Required Quest"
    )

    class Meta:
        managed = False
        db_table = "quest_prereqs"
        default_related_name = "prereq"
        ordering = ["quest", "required_quest"]
        verbose_name = "Quest Prerequisite"
        verbose_name_plural = "Quest Prerequisites"

    def __repr__(self) -> str:
        return f'Quest Prereq: "{self.__str__()}"'

    def __str__(self) -> str:
        return f"{self.quest} requires {self.required_quest}"
