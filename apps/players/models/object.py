from django.db import models

from apps.objects.models.object import Object
from .player import PlayerBase


class PositionType(models.IntegerChoices):
    """Ishar equipment position type choices."""
    NEGATIVE_ONE = -1
    EQUIPMENT = 0
    INVENTORY = 1
    UNUSED = 2
    INSIDE_OF_SOMETHING_ELSE = 3

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.value})"

    def __str__(self) -> str:
        return self.name.title()


class PositionValue(models.IntegerChoices):
    """Ishar equipment position value choices."""
    NEGATIVE_ONE = -1
    ZERO = 0
    WIELDING = 1
    HELD_IN_LEFT_HAND = 2
    HELD_IN_RIGHT_HAND = 3
    WIELDING_IN_TWO = 4
    EQUIPPED_ON_BODY = 5
    EQUIPPED_ON_HEAD = 6
    EQUIPPED_ON_NECK = 7
    EQUIPPED_ON_CHEST = 8
    EQUIPPED_ON_BACK = 9
    EQUIPPED_ON_ARMS = 10
    EQUIPPED_ON_RIGHT_WRIST = 11
    EQUIPPED_ON_LEFT_WRIST = 12
    EQUIPPED_ON_HANDS = 13
    EQUIPPED_ON_RIGHT_FINGER = 14
    EQUIPPED_ON_LEFT_FINGER = 15
    EQUIPPED_ON_WAIST = 16
    EQUIPPED_ON_LEGS = 17
    EQUIPPED_ON_FEET = 18
    EQUIPPED_ABOUT = 19
    EQUIPPED_ON_FACE = 20
    EQUIPPED_IN_MOUTH = 21
    EQUIPPED_ON_NECK_ALT = 22
    EQUIPPED_ON_BACK_ALT = 23
    EQUIPPED_ON_FOREHEAD = 24
    EQUIPPED_ON_UPPER_BODY = 25
    MAX_EQUIPPED = 26

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.value})"

    def __str__(self) -> str:
        return self.name.title()


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
        verbose_name="Object"
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
        choices=PositionType,
        null=True,
        help_text="Position type of the player object.",
        verbose_name="Position Type"
    )
    position_val = models.IntegerField(
        blank=True,
        choices=PositionValue,
        null=True,
        help_text="Position value of the player object.",
        verbose_name="Position Value"
    )
    parent_player_object = models.ForeignKey(
        blank=False,
        null=False,
        db_column="parent_player_object",
        default=0,
        help_text="Parent player object (container) of the player object.",
        on_delete=models.SET_DEFAULT,
        related_name="+",
        to="self",
        verbose_name="Container"
    )

    def is_contained(self) -> bool:
        if self.position_type == PositionType.INSIDE_OF_SOMETHING_ELSE:
            return True
        return False

    class Meta:
        managed = False
        db_table = "player_objects"
        default_related_name = "player_object"
        ordering = ("-position_type", "-position_val", "-pk")
        verbose_name = "Player Object"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return f"{self.object} @ {self.player}"
