from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property

from apps.core.models.textarea import NoStripTextareaField
from apps.skills.utils import SKILL_TYPE_NAMES, stat_name, strip_color

from .type.position import PlayerPosition
from .type.save import SkillSaveType
from .type.type import SkillType


class SkillManager(models.Manager):
    def get_by_natural_key(self, skill_name):
        """Natural key by skill name."""
        return self.get(skill_name=skill_name)


class Skill(models.Model):
    """Ishar skill (or "spell")."""

    id = models.AutoField(
        blank=False,
        db_column="id",
        editable=False,
        null=False,
        help_text="Auto-generated permanent ID number of the skill.",
        primary_key=True,
        verbose_name="ID",
    )
    enum_symbol = models.CharField(
        max_length=255,
        help_text="Internal ENUM symbol of the skill.",
        verbose_name="ENUM Symbol",
    )
    func_name = models.CharField(
        blank=True,
        max_length=255,
        null=True,
        help_text="Internal function name for the skill.",
        verbose_name="Function Name",
    )
    skill_name = models.TextField(
        blank=True,
        help_text="Friendly name of the skill.",
        null=True,
        verbose_name="Skill Name",
    )
    min_posn = models.IntegerField(
        blank=True,
        choices=PlayerPosition,
        null=True,
        help_text="Minimum position to use the skill.",
        verbose_name="Minimum Position",
    )
    min_use = models.IntegerField(
        blank=True,
        null=True,
        help_text="Minimum use of the skill.",
        verbose_name="Minimum Use",
    )
    spell_breakpoint = models.IntegerField(
        blank=True,
        null=True,
        help_text="Breakpoint of the spell related to the skill.",
        verbose_name="Spell Breakpoint",
    )
    held_cost = models.IntegerField(
        blank=True,
        null=True,
        help_text="Held cost of the skill.",
        verbose_name="Held Cost",
    )
    wearoff_msg = NoStripTextareaField(
        blank=True,
        null=True,
        help_text="Message shown to the user when the skill wears off.",
        verbose_name="Wear-off Message",
    )
    chant_text = models.TextField(
        blank=True,
        null=True,
        help_text="Text chanted to use the skill.",
        verbose_name="Chant Text",
    )
    difficulty = models.IntegerField(
        blank=True,
        null=True,
        help_text="Difficulty of the skill.",
        verbose_name="Difficulty",
    )
    rate = models.IntegerField(
        blank=True,
        null=True,
        help_text="Rate of the skill.",
        verbose_name="Rate"
    )
    notice_chance = models.IntegerField(
        blank=True,
        null=True,
        help_text="Notice chance of the skill.",
        verbose_name="Notice Chance",
    )
    appearance = models.TextField(
        blank=True,
        null=True,
        help_text="Appearance of the skill.",
        verbose_name="Appearance",
    )
    scale = models.IntegerField(
        blank=True, null=True, help_text="Scale of the skill.", verbose_name="Scale"
    )
    mod_stat_1 = models.IntegerField(
        blank=True,
        null=True,
        help_text="Mod stat 1 of the skill.",
        verbose_name="Mod Stat 1",
    )
    mod_stat_2 = models.IntegerField(
        blank=True,
        null=True,
        help_text="Mod stat 2 of the skill.",
        verbose_name="Mod Stat 2",
    )
    decide_func = models.TextField(
        blank=True,
        null=True,
        help_text="Internal function for decision-making for the skill.",
        verbose_name="Decide Function",
    )
    skill_type = models.IntegerField(
        choices=SkillType,
        help_text="Type of skill.",
        verbose_name="Skill Type",
    )
    parent_skill = models.ForeignKey(
        blank=True,
        db_column="parent_skill",
        db_default=-1,
        default=-1,
        help_text="Parent skill of skill.",
        null=True,
        on_delete=models.SET_DEFAULT,
        related_name="+",
        to="self",
        verbose_name="Parent Skill",
    )
    special_int = models.IntegerField(
        blank=True,
        default=-1,
        null=True,
        help_text="Integer that is special.",
        verbose_name="Special Integer",
    )
    obj_display = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        help_text="Display text of object related to the skill.",
        verbose_name="Object Display",
    )
    req_save = models.IntegerField(
        blank=True,
        choices=SkillSaveType,
        null=True,
        help_text="Required type of save for the skill.",
        verbose_name="Required Save",
    )
    # Cooldown num / size is dice.
    #   for example, 2d4 where 2 is num and 4 is size
    cooldown_num = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="Cool down number for the skill. (Dice X value: XdY)",
        verbose_name="Cool Down Number",
    )
    cooldown_size = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="Cool down size for the skill. (Dice Y value: XdY)",
        verbose_name="Cool Down Size",
    )
    ability_calc_func = models.TextField(
        blank=True,
        null=True,
        help_text="Ability calculation function for the skill.",
        verbose_name="Ability Calculation Function",
    )
    description = models.CharField(
        max_length=1080,
        blank=True,
        null=True,
        help_text="Textual description of the skill.",
        verbose_name="Description",
    )

    class Meta:
        db_table = "skills"
        default_related_name = "skill"
        ordering = ("skill_name",)
        managed = False
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self) -> str:
        return self.skill_name or self.enum_symbol

    def natural_key(self) -> str:
        """Natural key by skill name or ENUM symbol."""
        return self.skill_name

    def get_absolute_url(self) -> str:
        """URL to this skill's public page (anchored)."""
        return reverse("skill_page", args=(self.skill_name,)) + "#skill"

    # --- Display helpers (mirror the in-game ``skill`` command) -------------
    # These reproduce the non-player-specific facts from display_skill_full
    # (ishar-mud src/kernel/info.c) so the web page and the game agree.

    @property
    def type_name(self) -> str:
        """Game-faithful skill-type label (``skill_types[]``)."""
        return SKILL_TYPE_NAMES.get(self.skill_type, "")

    @property
    def is_spell(self) -> bool:
        return self.skill_type == SkillType.SPELL

    @property
    def is_skill(self) -> bool:
        return self.skill_type == SkillType.SKILL

    @property
    def description_display(self) -> str:
        """Description with game color codes stripped for web display."""
        return strip_color(self.description)

    @property
    def stat_pairing(self):
        """``(stat1, stat2)`` names when the skill pairs two distinct stats,
        else ``None`` — mirrors the 'Stat Pairing' line (skills only)."""
        if not self.is_skill:
            return None
        first, second = stat_name(self.mod_stat_1), stat_name(self.mod_stat_2)
        if first and second and first != second:
            return (first, second)
        return None

    @property
    def cooldown_display(self) -> str:
        """Cooldown text, mirroring display_skill_full: 'N seconds' when the
        size is 1, else 'NdM seconds'. Empty when there is no cooldown."""
        num = self.cooldown_num or 0
        if not num:
            return ""
        size = self.cooldown_size or 0
        if size == 1:
            return f"{num} second{'' if num == 1 else 's'}"
        return f"{num}d{size} seconds"

    @property
    def spell_flag_names(self) -> list:
        """Names of this skill's spell flags (via ``skills_spell_flags``)."""
        return [
            skill_flag.flag.name
            for skill_flag in self.flags.select_related("flag")
            if skill_flag.flag_id
        ]

    @cached_property
    def _flag_haystack(self) -> str:
        # Normalized (A-Z only) flag names joined for tolerant token checks —
        # spell_flags.name is game-seeded and its exact casing/spacing varies.
        import re

        return " ".join(
            re.sub(r"[^A-Z]", "", name.upper()) for name in self.spell_flag_names
        )

    @property
    def is_quick_action(self) -> bool:
        return "MELEE" in self._flag_haystack  # ALLOW_MELEE

    @property
    def movement_restricted(self) -> bool:
        return "NOMOVEMENT" in self._flag_haystack

    @property
    def is_breath(self) -> bool:
        return "BREATH" in self._flag_haystack

    @property
    def action_display(self) -> str:
        """'Quick Action' / 'Standard Action' for skills; '' otherwise."""
        if not self.is_skill:
            return ""
        return "Quick Action" if self.is_quick_action else "Standard Action"

    @property
    def command(self) -> str:
        """The command to invoke this ability, mirroring display_skill_full."""
        name = self.skill_name or ""
        if self.is_spell:
            return f"cast '{name}'"
        if self.is_breath:
            return f"breathe '{name}'"
        if self.is_skill:
            return f"action '{name}'"
        return ""
