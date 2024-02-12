from django.db import models

from ishar.apps.classes.models import Class
from ishar.apps.races.models.race import Race
from ishar.apps.players.models import Player


class PlayerGender(models.IntegerChoices):
    """
    Player character genders.
    """
    MALE = 1
    FEMALE = 2

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__, repr(self.__str__()), self.value
        )

    def __str__(self) -> str:
        return self.name


class PlayerCommon(models.Model):
    """
    Player common attributes for class, race, level, etc.
    """
    player = models.OneToOneField(
        db_column="player_id",
        help_text="Player character with common attributes.",
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="common",
        related_query_name="common",
        to=Player,
        to_field="id",
        verbose_name="Player"
    )
    player_class = models.ForeignKey(
        db_column="class_id",
        help_text="Class of the player character.",
        on_delete=models.CASCADE,
        related_query_name="+",
        to=Class,
        verbose_name="Class"
    )
    race = models.ForeignKey(
        db_column="race_id",
        help_text="Race of the player character.",
        on_delete=models.CASCADE,
        related_query_name="+",
        to=Race,
        verbose_name="Race"
    )
    sex = models.IntegerField(
        choices=PlayerGender,
        help_text="Sex/gender of the player character.",
        verbose_name="Sex/Gender"
    )
    level = models.PositiveIntegerField(
        help_text="Level of the player character.",
        verbose_name="Level"
    )
    weight = models.PositiveSmallIntegerField(
        help_text="Weight of the player character, in pounds.",
        verbose_name="Weight"
    )
    height = models.PositiveSmallIntegerField(
        help_text="Height of the player character, in inches.",
        verbose_name="Height"
    )
    comm_points = models.SmallIntegerField(
        help_text="Communication points of the player character.",
        verbose_name="Communication Points"
    )
    alignment = models.SmallIntegerField(
        help_text="Alignment of the player character.",
        verbose_name="Alignment"
    )
    strength = models.PositiveIntegerField(
        help_text="Strength of the player character.",
        verbose_name="Strength"
    )
    agility = models.PositiveIntegerField(
        help_text="Agility of the player character.",
        verbose_name="Agility"
    )
    endurance = models.PositiveIntegerField(
        help_text="Endurance of the player character.",
        verbose_name="Endurance"
    )
    perception = models.PositiveIntegerField(
        help_text="Perception of the player character.",
        verbose_name="Perception"
    )
    focus = models.PositiveIntegerField(
        help_text="Focus of the player character.",
        verbose_name="Focus"
    )
    willpower = models.PositiveIntegerField(
        help_text="Willpower of the player character.",
        verbose_name="Willpower"
    )
    init_strength = models.PositiveIntegerField(
        help_text="Initial strength of the player character.",
        verbose_name="Initial Strength"
    )
    init_agility = models.PositiveIntegerField(
        help_text="Initial agility of the player character.",
        verbose_name="Initial Agility"
    )
    init_endurance = models.PositiveIntegerField(
        help_text="Initial endurance of the player character.",
        verbose_name="Initial Endurance"
    )
    init_perception = models.PositiveIntegerField(
        help_text="Initial perception of the player character.",
        verbose_name="Initial Perception"
    )
    init_focus = models.PositiveIntegerField(
        help_text="Initial focus of the player character.",
        verbose_name="Initial Focus"
    )
    init_willpower = models.PositiveIntegerField(
        help_text="Initial willpower of the player character.",
        verbose_name="Initial Willpower"
    )
    perm_hit_pts = models.SmallIntegerField(
        help_text="Permanent hit points of the player character.",
        verbose_name="Permanent Hit Points"
    )
    perm_move_pts = models.SmallIntegerField(
        help_text="Permanent movement points of the player character.",
        verbose_name="Permanent Movement Points"
    )
    perm_spell_pts = models.SmallIntegerField(
        help_text="Permanent spell points of the player character.",
        verbose_name="Permanent Spell Points"
    )
    perm_favor_pts = models.SmallIntegerField(
        help_text="Permanent favor points of the player character.",
        verbose_name="Permanent Favor Points"
    )
    curr_hit_pts = models.SmallIntegerField(
        help_text="Current hit points of the player character.",
        verbose_name="Current Hit Points"
    )
    curr_move_pts = models.SmallIntegerField(
        help_text="Current movement points of the player character.",
        verbose_name="Current Movement Points"
    )
    curr_spell_pts = models.SmallIntegerField(
        help_text="Current spell points of the player character.",
        verbose_name="Current Spell Points"
    )
    curr_favor_pts = models.SmallIntegerField(
        help_text="Current favor points of the player character.",
        verbose_name="Current Favor Points"
    )
    experience = models.IntegerField(
        help_text="Experience points for the player character.",
        verbose_name="Experience"
    )
    gold = models.IntegerField(
        help_text="Value of gold that the player character has.",
        verbose_name="Gold"
    )
    karma = models.IntegerField(
        help_text="Karma value for the player character.",
        verbose_name="Karma"
    )

    class Meta:
        managed = False
        db_table = "player_common"
        default_related_name = "common"
        ordering = ("player_id",)
        verbose_name = "Player Common"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}: {repr(self.__str__())} ({self.id})"
        )

    def __str__(self) -> str:
        return self.player.name
