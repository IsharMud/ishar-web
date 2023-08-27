from django.db import models


class Quest(models.Model):
    """
    Quest playable by a player character.
    """
    quest_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated permanent unique quest number.",
        verbose_name="Quest ID"
    )
    name = models.CharField(
        unique=True,
        max_length=25,
        help_text="Internal name of the quest.",
        verbose_name="Name"
    )
    display_name = models.CharField(
        max_length=30,
        help_text="Friendly display name of the quest.",
        verbose_name="Display Name"
    )
    completion_message = models.CharField(
        max_length=700,
        help_text="Message sent to the player upon completion of the quest.",
        verbose_name="Completion Message"
    )
    min_level = models.IntegerField(
        help_text="Minimum level of a player that may partake in the quest.",
        verbose_name="Minimum Level"
    )
    max_level = models.IntegerField(
        help_text="Maximum level of a player that may partake in the quest.",
        verbose_name="Maximum Level"
    )
    repeatable = models.IntegerField(
        help_text="Is the quest repeatable?",
        verbose_name="Repeatable"
    )
    description = models.CharField(
        max_length=512,
        help_text="Description of the quest.",
        verbose_name="Description"
    )
    prerequisite = models.IntegerField(
        help_text="Prerequisite quest ID number before this quest can be done.",
        verbose_name="Prerequisite"
    )
    class_restrict = models.IntegerField(
        help_text="Player class ID number to which the quest is restricted.",
        verbose_name="Class Restrict"
    )
    quest_intro = models.CharField(
        max_length=2000,
        help_text="Introduction text for the quest.",
        verbose_name="Quest Intro"
    )
    quest_source = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Quest source.",
        verbose_name="Quest Source"
    )
    quest_return = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Quest return.",
        verbose_name="Quest Return"
    )

    def _is_repeatable(self):
        """
        Boolean whether the quest is repeatable.
        """
        if self.repeatable == 1:
            return True
        return False

    _is_repeatable.boolean = True
    is_repeatable = property(_is_repeatable)

    def __repr__(self) -> str:
        return f'Quest: "{self.display_name}" ({self.quest_id})'

    def __str(self) -> str:
        return self.display_name

    class Meta:
        managed = False
        db_table = 'quests'
