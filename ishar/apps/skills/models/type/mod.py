from django.db.models import IntegerChoices


class SkillModType(IntegerChoices):
    """
    Skill mod types.
    """
    NONE = 0, "None"
    NEGATIVE_ONE = -1, "Negative One"
    STRENGTH = 1, "Strength"
    PERCEPTION = 2, "Perception"
    FOCUS = 3, "Focus"
    AGILITY = 4, "Agility"
    ENDURANCE = 5, "Endurance"
    WILLPOWER = 6, "Willpower"
    SPEED = 7, "Speed"
    SEX = 8, "Sex"
    AGE = 9, "Age"
    WEIGHT = 10, "Weight"
    HEIGHT = 11, "Height"
    SPELL_POINTS = 12, "Spell Points"
    HIT_POINTS = 13, "Hit Points"
    MOVE_POINTS = 14, "Move Points"
    ARMOR = 15, "Armor"
    ATTACK = 16, "Attack"
    DAMAGE = 17, "Melee Damage"
    HEAL = 18, "Heal"
    SAVE_POISON = 19, "Fortitude"
    SAVE_PETRIFICATION = 20, "Fortitude"
    SAVE_BREATH = 21, "Reflex"
    SAVE_MAGIC = 22, "Resilience"
    ALIGNMENT = 23, "Alignment"
    LIGHT_IN = 24, "Light In"
    LIGHT_ON = 25, "Light On"
    FIRESHIELD = 26, "Fireshield"
    SAVE_ILLUSION = 27, "Resilience"
    HEAL_HIT = 28, "Heal Hit"
    HEAL_SPELL = 29, "Heal Spell"
    HEAL_MOVE = 30, "Heal Move"
    HEAL_FAVOR = 31, "Heal Favor"
    SAVE_ALL = 32, "Save All"
    CRITICAL = 33, "Critical"
    BODY = 34, "Body"
    MIND = 35, "Mind"
    XP = 36, "Experience"
    SAVE_DISTRACTION = 37, "Resilience"
    SUSTAIN_SPELL = 38, "Sustained Spell"
    EXPERTISE = 39, "Expertise"
    SAVE_FORTITUDE = 40, "Fortitude"
    SAVE_REFLEX = 41, "Reflex"
    SAVE_RESILIENCE = 42, "Resilience"
    SPELL_POTENCY = 43, "Spell Potency"
    RESISTANCE = 44, "Resistance"
    SPELL_DAMAGE = 45, "Spell Damage"
    HEALING_POWER = 46, "Healing Power"
    SUSCEPTIBILITY = 47, "Susceptibility"
    IMMUNITY = 48, "Immunity"
    VULNERABILITY = 49, "Vulnerability"

    def __repr__(self) -> str:
        return "%s: %s (%i)" % (
            self.__class__.__name__, repr(self.__str__()), self.value
        )

    def __str__(self) -> str:
        return self.name
