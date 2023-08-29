from django.contrib import admin
from django.db import models

from .force import Force
from .spell import SpellInfo


class Race(models.Model):
    """
    Race.
    """
    race_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated primary identification number of the race.",
        verbose_name="Race ID"
    )
    symbol = models.CharField(
        max_length=100, blank=True, null=True,
        help_text="Internal symbol for the race.",
        verbose_name="Symbol"
    )
    display_name = models.CharField(
        max_length=25, blank=True, null=True,
        help_text="Friendly display name for the race.",
        verbose_name="Display Name"
    )
    folk_name = models.CharField(
        max_length=25, blank=True, null=True,
        help_text="Friendly folk name for the race.",
        verbose_name="Folk Name"

    )
    default_movement = models.CharField(
        max_length=10, blank=True, null=True,
        help_text="Default movement for the race.",
        verbose_name="Default Movement"
    )
    description = models.CharField(
        max_length=80, blank=True, null=True,
        help_text="Description of the race.",
        verbose_name="Description"
    )
    default_height = models.SmallIntegerField(
        blank=True, null=True,
        help_text="Description of the race.",
        verbose_name="Description"
    )
    default_weight = models.SmallIntegerField(
        blank=True, null=True,
        help_text="Default weight of the race.",
        verbose_name="Default Weight"
    )
    bonus_fortitude = models.SmallIntegerField(
        blank=True, null=True,
        help_text="Bonus fortitude for the race.",
        verbose_name="Bonus Fortitude"
    )
    bonus_reflex = models.SmallIntegerField(
        blank=True, null=True,
        help_text="Bonus reflex for the race.",
        verbose_name="Bonus Reflex"
    )
    bonus_resilience = models.SmallIntegerField(
        blank=True, null=True,
        help_text="Bonus resilience for the race.",
        verbose_name="Bonus Resilience"
    )
    listen_sound = models.CharField(
        max_length=80, blank=True, null=True,
        help_text="Listen sound for the race.",
        verbose_name="Listen Sound"
    )
    height_bonus = models.SmallIntegerField(
        blank=True, null=True,
        help_text="Height bonus for the race.",
        verbose_name="Height Bonus"
    )
    weight_bonus = models.SmallIntegerField(
        blank=True, null=True,
        help_text="Weight bonus for the race.",
        verbose_name="Weight Bonus"
    )
    short_description = models.CharField(
        max_length=80, blank=True, null=True,
        help_text="Short description of the race.",
        verbose_name="Short Description"
    )
    long_description = models.CharField(
        max_length=512, blank=True, null=True,
        help_text="Long description of the race.",
        verbose_name="Long Description"
    )
    attack_noun = models.CharField(
        max_length=25, blank=True, null=True,
        help_text="Attack noun for the race.",
        verbose_name="Attack Noun"
    )
    attack_type = models.SmallIntegerField(
        blank=True, null=True,
        help_text="Attack type for the race.",
        verbose_name="Attack Type"
    )
    vulnerabilities = models.TextField(
        blank=True, null=True,
        help_text="Vulnerabilities of the race.",
        verbose_name="Vulnerabilities"
    )
    susceptibilities = models.TextField(
        blank=True, null=True,
        help_text="Susceptibilities of the race.",
        verbose_name="susceptibilities"
    )
    resistances = models.TextField(
        blank=True, null=True,
        help_text="Resistances of the race.",
        verbose_name="Resistances"
    )
    immunities = models.TextField(
        blank=True, null=True,
        help_text="Immunities of the race.",
        verbose_name="Immunities"
    )
    additional_str = models.SmallIntegerField(
        blank=True, null=True,
        help_text="Additional strength of the race.",
        verbose_name="Additional Strength"
    )
    additional_agi = models.SmallIntegerField(
        blank=True, null=True,
        help_text="Additional agility of the race.",
        verbose_name="Additional Agility"
    )
    additional_end = models.SmallIntegerField(
        blank=True, null=True,
        help_text="Additional endurance of the race.",
        verbose_name="Additional Endurance"
    )
    additional_per = models.SmallIntegerField(
        blank=True, null=True,
        help_text="Additional perception of the race.",
        verbose_name="Additional Perception"
    )
    additional_foc = models.SmallIntegerField(
        blank=True, null=True,
        help_text="Additional focus of the race.",
        verbose_name="Additional Focus"
    )
    additional_wil = models.SmallIntegerField(
        blank=True, null=True,
        help_text="Additional willpower of the race.",
        verbose_name="Additional Willpower"
    )
    is_playable = models.IntegerField(
        blank=True, null=True,
        choices=[(0, False), (1, True)],
        help_text="Is the race playable by regular player characters?",
        verbose_name="Is Playable?"
    )
    is_humanoid = models.IntegerField(
        choices=[(0, False), (1, True)],
        help_text="Is the race humanoid?",
        verbose_name="Is Humanoid?"
    )
    is_invertebrae = models.IntegerField(
        choices=[(0, False), (1, True)],
        help_text="Is the race an invertebrate?",
        verbose_name="Is Invertebrae?"
    )
    is_flying = models.IntegerField(
        choices=[(0, False), (1, True)],
        help_text="Does the race fly?",
        verbose_name="Is Flying?"
    )
    is_swimming = models.IntegerField(
        choices=[(0, False), (1, True)],
        help_text="Does the race swim?",
        verbose_name="Is Swimming?"
    )
    darkvision = models.IntegerField(
        choices=[(0, False), (1, True)],
        help_text="Does the race have darkvision?",
        verbose_name="Darkvision?"
    )
    see_invis = models.IntegerField(
        choices=[(0, False), (1, True)],
        help_text="Can the race see invisibility?",
        verbose_name="See Invisibility?"
    )
    is_walking = models.IntegerField(
        help_text="Does the race walk?",
        verbose_name="Is Walking?"
    )
    endure_heat = models.IntegerField(
        choices=[(0, False), (1, True)],
        help_text="Can the race endure heat?",
        verbose_name="Endure Heat?"
    )
    endure_cold = models.IntegerField(
        choices=[(0, False), (1, True)],
        help_text="Can the race endure heat?",
        verbose_name="Endure Heat?"
    )
    is_undead = models.IntegerField(
        choices=[(0, False), (1, True)],
        help_text="Is the race undead?",
        verbose_name="Is Undead?"
    )

    class Meta:
        managed = False
        db_table = 'races'
        ordering = ["-is_playable", "display_name", "symbol", "race_id"]
        verbose_name = "Race"
        verbose_name_plural = "Races"

    def __repr__(self):
        return f"Race: {repr(self.__str__())} ({self.race_id})"

    def __str__(self):
        return self.display_name

    @admin.display(boolean=True, description="Playable", ordering="is_playable")
    def _is_playable(self) -> bool:
        """
        Boolean whether race can be chosen by player characters.
        """
        if self.is_playable == 1:
            return True
        return False


class RaceSkill(models.Model):
    race = models.ForeignKey(
        to=Race,
        on_delete=models.CASCADE
    )
    skill = models.ForeignKey(
        to=SpellInfo,
        on_delete=models.CASCADE
    )
    level = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'races_skills'


class RacialAffinity(models.Model):
    """
    Racial Affinity.
    """
    race = models.ForeignKey(
        to=Race,
        on_delete=models.CASCADE,
        help_text="Race of the racial affinity.",
        related_name="affinities",
        related_query_name="affinity",
        verbose_name="Affinity Type"
    )
    force = models.ForeignKey(
        to=Force,
        on_delete=models.CASCADE,
        help_text="Force of the racial affinity.",
        verbose_name="Force"
    )
    affinity_type = models.IntegerField(
        help_text="Type of racial affinity.",
        verbose_name="Affinity Type"
    )

    class Meta:
        managed = False
        db_table = 'racial_affinities'
        ordering = ("affinity_type",)
        verbose_name = "Racial Affinity"
        verbose_name_plural = "Racial Affinities"
