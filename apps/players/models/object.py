from django.db import models

from apps.objects.models.object import Object

from .player import PlayerBase


class PlayerObject(models.Model):

    player_objects_id = models.AutoField(
        primary_key=True,
        help_text = "Primary key player object identification number.",
        verbose_name = "Player Object ID"
    )
    player = models.ForeignKey(
        to=PlayerBase,
        on_delete=models.DO_NOTHING,
        help_text="Player related to the object.",
        verbose_name="Player",
        blank=True,
        null=True
    )
    object = models.ForeignKey(
        help_text='Identification number ("VNUM") of the object.',
        on_delete=models.DO_NOTHING,
        to=Object,
        to_field="vnum",
        verbose_name='Object ID ("VNUM")',
        blank=True,
        null=True
    )
    enchant = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Enchantment of the player object.",
        verbose_name="Enchant"
    )
    timer = models.IntegerField(
        blank=True,
        null=True,
        help_text="Timer of the player object.",
        verbose_name="Timer"
    )
    bound = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Bound (value) of the player object.",
        verbose_name="Bound"
    )
    state = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="State of the player object.",
        verbose_name="State"
    )
    min_level = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Minimum level of the player object.",
        verbose_name="Minimum Level"
    )
    val0 = models.IntegerField(
        blank=True,
        null=True,
        help_text="Value #0 of the player object.",
        verbose_name="Value #0"
    )
    val1 = models.IntegerField(
        blank=True,
        null=True,
        help_text="Value #1 of the player object.",
        verbose_name="Value #1"
    )
    val2 = models.IntegerField(
        blank=True,
        null=True,
        help_text="Value #2 of the player object.",
        verbose_name="Value #2"
    )
    val3 = models.IntegerField(
        blank=True,
        null=True,
        help_text="Value #3 of the player object.",
        verbose_name="Value #3"
    )
    position_type = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Position type of the player object.",
        verbose_name="Position type"
    )
    position_val = models.IntegerField(
        blank=True,
        null=True,
        help_text="Position value of the player object.",
        verbose_name="Position Value"
    )
    parent_player_object = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Parent player object, of the player object.",
        verbose_name="Parent Player Object"
    )

    class Meta:
        managed = False
        db_table = "player_objects"
        default_related_name = "player_object"
        ordering = ("-player_objects_id",)
        verbose_name = "Player Object"
        verbose_name_plural = "Player's Objects"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return f"{self.object} @ {self.player}"
