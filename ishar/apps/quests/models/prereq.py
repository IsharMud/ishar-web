from django.db import models

from .quest import Quest


class QuestPrereq(models.Model):
    """
    Quest Prerequisite.
    """
    quest_prereqs_id = models.AutoField(
        blank=False,
        db_column="quest_prereqs_id",
        help_text="Auto-generated, permanent quest pre-requisite relation ID.",
        primary_key=True,
        null=False,
        verbose_name="Quest Prerequisite ID"
    )
    quest = models.ForeignKey(
        to=Quest,
        on_delete=models.DO_NOTHING,
        db_column="quest_id",
        help_text="Quest which requires a prerequisite.",
        verbose_name="Quest"
    )
    required_quest = models.ForeignKey(
        to=Quest,
        on_delete=models.DO_NOTHING,
        db_column="required_quest",
        help_text="Prerequisite quest, required prior to another quest.",
        related_name="questprereq_required_quest_set",
        verbose_name="Required Quest"
    )

    class Meta:
        managed = False
        db_table = "quest_prereqs"
        ordering = ("quest", "required_quest")
        verbose_name = "Prerequisite"
        verbose_name_plural = "Prerequisites"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self) -> str:
        return "%s requires %s" % (self.quest, self.required_quest)
