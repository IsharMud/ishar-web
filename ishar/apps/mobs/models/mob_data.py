from django.db import models

from ishar.apps.classes.models import Class

from ishar.apps.players.models.gender import PlayerGender
from ishar.apps.races.models.race import Race
from ishar.apps.skills.models.type.position import PlayerPosition


class MobData(models.Model):
    """
    Mob data.
    """
    id = models.AutoField(
        blank=False,
        db_column="id",
        editable=False,
        null=False,
        help_text="Auto-generated ID number of the mob data row.",
        primary_key=True,
        verbose_name="Mob Data ID"
    )
    name = models.CharField(
        max_length=100,
        help_text="Name of the mob.",
        verbose_name="Name"
    )
    long_name = models.CharField(
        max_length=100,
        help_text="Long name of the mob.",
        verbose_name="Long Name"
    )
    room_desc = models.CharField(
        max_length=100,
        help_text="Room description for the mob.",
        verbose_name="Room Description"
    )
    description = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        help_text="Description of the mob.",
        verbose_name="Description"
    )
    spec_func = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Special function of the mob.",
        verbose_name="Special Function"
    )
    position = models.PositiveIntegerField(
        blank=True,
        choices=PlayerPosition,
        null=True,
        help_text="Position of the mob.",
        verbose_name="Position"
    )
    l_position = models.PositiveIntegerField(
        blank=True,
        choices=PlayerPosition,
        null=True,
        help_text="L position of the mob.",
        verbose_name="L Position"
    )
    damage_dice_number = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="Damage dice number for the mob.",
        verbose_name="Damage Dice Number"
    )
    damage_dice_size = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="Damage dice size for the mob.",
        verbose_name="Damage Dice Size"
    )
    extra_armor = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Extra armor amount for the mob.",
        verbose_name="Extra Armor"
    )
    additional_health_heal = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Additional health heal amount for the mob.",
        verbose_name="Additional Health Heal"
    )
    additional_move_heal = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Additional move heal amount for the mob.",
        verbose_name="Additional Move Heal"
    )
    additional_mana_heal = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Additional mana heal amount for the mob.",
        verbose_name="Additional Mana Heal"
    )
    additional_favor_heal = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Additional favor heal amount for the mob.",
        verbose_name="Additional Favor Heal"
    )
    additional_damage = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Additional damage amount for the mob.",
        verbose_name="Additional Damage"
    )
    additional_speed = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Additional speed amount for the mob.",
        verbose_name="Additional Speed"
    )
    additional_alignment = models.IntegerField(
        blank=True,
        null=True,
        help_text="Additional alignment amount for the mob.",
        verbose_name="Additional Alignment"
    )
    armor = models.IntegerField(
        blank=True,
        null=True,
        help_text="Armor amount for the mob.",
        verbose_name="Armor"
    )
    attack = models.IntegerField(
        blank=True,
        null=True,
        help_text="Attack amount for the mob.",
        verbose_name="Attack"
    )
    sex = models.PositiveIntegerField(
        blank=True,
        choices=PlayerGender,
        null=True,
        help_text="Sex/gender of the mob.",
        verbose_name="Sex"
    )
    race = models.ForeignKey(
        to=Race,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Race of the mob.",
        verbose_name="Race"
    )
    mob_class = models.ForeignKey(
        to=Class,
        on_delete=models.SET_NULL,
        db_column="class_id",
        blank=True,
        null=True,
        help_text="Class of the mob.",
        verbose_name="Class"
    )  # Field renamed because it was a Python reserved word.
    level = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Level of the mob.",
        verbose_name="Level"
    )
    weight = models.PositiveSmallIntegerField(
        help_text="Weight of the mob.",
        verbose_name="Weight"
    )
    height = models.PositiveSmallIntegerField(
        help_text="Height of the mob.",
        verbose_name="Height"
    )
    comm_points = models.SmallIntegerField(
        help_text="Communication points of the mob.",
        verbose_name="Communication Points"
    )
    alignment = models.SmallIntegerField(
        help_text="Alignment of the mob.",
        verbose_name="Alignment"
    )
    strength = models.PositiveIntegerField(
        help_text="Strength of the mob.",
        verbose_name="Strength"
    )
    agility = models.PositiveIntegerField(
        help_text="Agility of the mob.",
        verbose_name="Agility"
    )
    endurance = models.PositiveIntegerField(
        help_text="Endurance of the mob.",
        verbose_name="Endurance"
    )
    perception = models.PositiveIntegerField(
        help_text="Perception of the mob.",
        verbose_name="Perception"
    )
    focus = models.PositiveIntegerField(
        help_text="Focus of the mob.",
        verbose_name="Focus"
    )
    willpower = models.PositiveIntegerField(
        help_text="Willpower",
        verbose_name="Willpower of the mob."
    )
    init_strength = models.PositiveIntegerField(
        help_text="Initial strength amount for the mob.",
        verbose_name="Initial Strength"
    )
    init_agility = models.PositiveIntegerField(
        help_text="Initial agility amount for the mob.",
        verbose_name="Initial Agility"
    )
    init_endurance = models.PositiveIntegerField(
        help_text="Initial endurance amount for the mob.",
        verbose_name="Initial Endurance"
    )
    init_perception = models.PositiveIntegerField(
        help_text="Initial perception amount for the mob.",
        verbose_name="Initial Perception"
    )
    init_focus = models.PositiveIntegerField(
        help_text="Initial focus amount for the mob.",
        verbose_name="Initial Focus"
    )
    init_willpower = models.PositiveIntegerField(
        help_text="Initial willpower amount for the mob.",
        verbose_name="Initial Willpower"
    )
    perm_hit_pts = models.SmallIntegerField(
        help_text="Permanent hit points of the mob.",
        verbose_name="Permanent Hit Points"
    )
    perm_move_pts = models.SmallIntegerField()
    perm_spell_pts = models.SmallIntegerField(
        help_text="Permanent spell points of the mob.",
        verbose_name="Permanent Spell Points"
    )
    perm_favor_pts = models.SmallIntegerField(
        help_text="Permanent favor points of the mob.",
        verbose_name="Permanent Favor Points"
    )
    curr_hit_pts = models.SmallIntegerField(
        help_text="Current hit points of the mob.",
        verbose_name="Current Hit Points"
    )
    curr_move_pts = models.SmallIntegerField(
        help_text="Current move points of the mob.",
        verbose_name="Current Move Points"
    )
    curr_spell_pts = models.SmallIntegerField(
        help_text="Current spell points of the mob.",
        verbose_name="Current Spell Points"
    )
    curr_favor_pts = models.SmallIntegerField(
        help_text="Current favor points of the mob.",
        verbose_name="Current Favor Points"
    )
    experience = models.IntegerField(
        help_text="Experience for the mob.",
        verbose_name="Experience"
    )
    gold = models.IntegerField(
        help_text="Gold amount for the mob.",
        verbose_name="Gold"
    )
    karma = models.IntegerField(
        help_text="Karma amount for the mob.",
        verbose_name="Karma"
    )

    class Meta:
        managed = False
        db_table = "mob_data"
        default_related_name = "mobile"
        ordering = ("name",)
        verbose_name = "Mobile"
        verbose_name_plural = "Mobiles"

    def __repr__(self) -> str:
        return "%s: %s [%d]" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self) -> str:
        return "%s (Level %i)" % (
            self.long_name or self.name,
            self.level
        )
