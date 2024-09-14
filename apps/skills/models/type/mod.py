from django.db.models import IntegerChoices


class SkillModType(IntegerChoices):
    """Skill mod type choices."""
    ZERO = 0
    NEGATIVE_ONE = -1
    STRENGTH = 1
    PERCEPTION = 2
    FOCUS = 3
    AGILITY = 4
    ENDURANCE = 5
    WILLPOWER = 6
    SPEED = 7
    SEX = 8
    AGE = 9
    WEIGHT = 10
    HEIGHT = 11
    SPELL_POINTS = 12
    HIT_POINTS = 13
    MOVE_POINTS = 14
    ARMOR = 15
    ATTACK = 16
    DAMAGE = 17
    HEAL = 18
    SAVE_POISON = 19
    SAVE_PETRIFICATION = 20
    SAVE_BREATH = 21
    SAVE_MAGIC = 22
    ALIGNMENT = 23
    LIGHT_IN = 24
    LIGHT_ON = 25
    FIRESHIELD = 26
    SAVE_ILLUSION = 27
    HEAL_HIT = 28
    HEAL_SPELL = 29
    HEAL_MOVE = 30
    HEAL_FAVOR = 31
    SAVE_ALL = 32
    CRITICAL = 33
    BODY = 34
    MIND = 35
    EXPERIENCE = 36
    SAVE_DISTRACTION = 37
    SUSTAIN_SPELL = 38
    EXPERTISE = 39
    SAVE_FORTITUDE = 40
    SAVE_REFLEX = 41
    SAVE_RESILIENCE = 42
    SPELL_POTENCY = 43,
    RESISTANCE = 44
    SPELL_DAMAGE = 45
    HEALING_POWER = 46
    SUSCEPTIBILITY = 47
    IMMUNITY = 48
    VULNERABILITY = 49

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.__str__()} ({self.value})"

    def __str__(self) -> str:
        return self.name.title()
