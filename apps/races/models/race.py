from django.db import models


class RaceManager(models.Manager):
    def get_by_natural_key(self, display_name):
        # Natural key by race display name.
        return self.get(display_name=display_name)


class Race(models.Model):
    """Ishar race."""

    objects = RaceManager()

    race_id = models.AutoField(
        primary_key=True,
        help_text="Auto-generated primary identification number of the race.",
        verbose_name="Race ID",
    )
    symbol = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Internal symbol for the race.",
        verbose_name="Symbol",
    )
    display_name = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        help_text="Friendly display name for the race.",
        verbose_name="Display Name",
    )
    folk_name = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        help_text="Friendly folk name for the race.",
        verbose_name="Folk Name",
    )
    default_movement = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Default movement for the race.",
        verbose_name="Default Movement",
    )
    description = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        help_text="Description of the race.",
        verbose_name="Description",
    )
    default_height = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Default height of the race, in inches.",
        verbose_name="Default Height",
    )
    default_weight = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Default weight of the race, in pounds.",
        verbose_name="Default Weight",
    )
    bonus_fortitude = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Bonus fortitude for the race.",
        verbose_name="Bonus Fortitude",
    )
    bonus_reflex = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Bonus reflex for the race.",
        verbose_name="Bonus Reflex",
    )
    bonus_resilience = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Bonus resilience for the race.",
        verbose_name="Bonus Resilience",
    )
    listen_sound = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        help_text="Listen sound for the race.",
        verbose_name="Listen Sound",
    )
    height_bonus = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Height bonus for the race.",
        verbose_name="Height Bonus",
    )
    weight_bonus = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Weight bonus for the race.",
        verbose_name="Weight Bonus",
    )
    short_description = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        help_text="Short description of the race.",
        verbose_name="Short Description",
    )
    long_description = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text="Long description of the race.",
        verbose_name="Long Description",
    )
    attack_noun = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        help_text="Attack noun for the race.",
        verbose_name="Attack Noun",
    )
    attack_type = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Attack type for the race.",
        verbose_name="Attack Type",
    )
    additional_str = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Additional strength of the race.",
        verbose_name="Additional Strength",
    )
    additional_agi = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Additional agility of the race.",
        verbose_name="Additional Agility",
    )
    additional_end = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Additional endurance of the race.",
        verbose_name="Additional Endurance",
    )
    additional_per = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Additional perception of the race.",
        verbose_name="Additional Perception",
    )
    additional_foc = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Additional focus of the race.",
        verbose_name="Additional Focus",
    )
    additional_wil = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text="Additional willpower of the race.",
        verbose_name="Additional Willpower",
    )
    is_playable = models.BooleanField(
        help_text="Is the race playable by regular player characters?",
        verbose_name="Is Playable?",
    )
    is_humanoid = models.BooleanField(
        help_text="Is the race humanoid?",
        verbose_name="Is Humanoid?",
    )
    is_invertebrae = models.BooleanField(
        help_text="Is the race an invertebrate?",
        verbose_name="Is Invertebrae?",
    )
    is_flying = models.BooleanField(
        help_text="Does the race fly?",
        verbose_name="Is Flying?",
    )
    is_swimming = models.BooleanField(
        help_text="Does the race swim?",
        verbose_name="Is Swimming?",
    )
    darkvision = models.BooleanField(
        help_text="Does the race have darkvision?",
        verbose_name="Darkvision?",
    )
    see_invis = models.BooleanField(
        help_text="Can the race see invisibility?",
        verbose_name="See Invisibility?",
    )
    is_walking = models.BooleanField(
        help_text="Does the race walk?",
        verbose_name="Is Walking?",
    )
    endure_heat = models.BooleanField(
        help_text="Can the race endure heat?",
        verbose_name="Endure Heat?",
    )
    endure_cold = models.BooleanField(
        help_text="Can the race endure cold?",
        verbose_name="Endure Cold?",
    )
    is_undead = models.BooleanField(
        help_text="Is the race undead?",
        verbose_name="Is Undead?",
    )

    class Meta:
        managed = False
        db_table = "races"
        default_related_name = "race"
        ordering = ("-is_playable", "display_name")
        verbose_name = "Race"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.display_name

    def natural_key(self) -> str:
        # Natural key by display name.
        return self.display_name
