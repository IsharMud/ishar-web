"""Helpers for the public skill/spell pages.

Constants here mirror the game engine (ishar-mud) so the web renders the same
facts the in-game ``skill`` command (``display_skill_full``) shows.
"""
import re


# Primary stats, 0-indexed to match the game's ``statnames[]``
# (ishar-mud src/kernel/constants.c). ``skills.mod_stat_1`` / ``mod_stat_2``
# index into this array.
STAT_NAMES = (
    "Strength", "Perception", "Focus", "Agility", "Endurance", "Willpower",
)

# ``skill_type`` -> label, matching the game's ``skill_types[]`` (same file).
# The DB column is a tinyint that ranges wider than the Django ``SkillType``
# enum (0..3), so map the full game range for display.
SKILL_TYPE_NAMES = {
    0: "Passive", 1: "Skill", 2: "Spell", 3: "Craft", 4: "Enchant", 5: "Passive",
}

# Ishar in-band color codes are "@c" followed by one code character.
_COLOR_RE = re.compile(r"@c.")


def strip_color(text: str) -> str:
    """Strip Ishar ``@cX`` color codes from game text for clean web display."""
    if not text:
        return ""
    return _COLOR_RE.sub("", text).replace("@@", "@")


def stat_name(index) -> str:
    """Name of a primary stat by its 0-based index, or '' if out of range."""
    if index is None or index < 0 or index >= len(STAT_NAMES):
        return ""
    return STAT_NAMES[index]


# Skill types a normal mortal sees in the game's skill list. Values are the
# game's ``skill_types_t`` enum (ishar-mud constants.h): TYPE=0, SKILL=1,
# SPELL=2, CRAFT=3, ENCHANT=4, PASSIVE=5. The `skills` command shows only
# SKILL/SPELL/PASSIVE — CRAFT and ENCHANT are professions surfaced elsewhere,
# and TYPE is an internal marker (info.c). Excluding these is what keeps
# deprecated enchants out of the class lists.
VISIBLE_SKILL_TYPES = (1, 2, 5)  # SKILL_SKILL, SPELL_SKILL, PASSIVE_SKILL

# Skills gated to a not-yet-live season while the active season's
# ``new_features_on`` is off (ishar-mud person.c). Matched on ``enum_symbol``.
SEASON_GATED_ENUM_SYMBOLS = (
    "SPELL_VIVISECT", "SPELL_SYNAPSE_SHOCK", "SPELL_FRENZY", "SPELL_MIASMA",
    "SPELL_CORPSE_EXPLOSION", "SPELL_PSYCHIC_HEMORRHAGE",
    "SPELL_EYES_OF_THE_MASTER", "SPELL_AVOW", "METAMAGIC_CLARITY",
    "METAMAGIC_HELD_SPELL", "METAMAGIC_EXPAND", "METAMAGIC_QUICKEN",
    "METAMAGIC_RUINOUS",
)


def learnable_skill_ids() -> set:
    """Skill IDs a *playable* class or race can currently learn, mirroring the
    game's ``can_class_learn_skill`` / ``can_race_learn_skill`` >= 0: a class
    row with ``min_level >= 0`` and ``max_learn > 0``, or a race row with
    ``level >= 0``. Deprecated rows (``max_learn <= 0``) are excluded here, the
    same way the game hides them from mortal skill lists.
    """
    from apps.classes.models.skill import ClassSkill
    from apps.races.models.skill import RaceSkill

    class_ids = ClassSkill.objects.filter(
        player_class__is_playable=True, min_level__gte=0, max_learn__gt=0,
    ).values_list("skill_id", flat=True)
    race_ids = RaceSkill.objects.filter(
        race__is_playable=True, level__gte=0,
    ).values_list("skill_id", flat=True)
    return set(class_ids) | set(race_ids)


def _new_features_on() -> bool:
    # Whether the active season has its gated new features enabled.
    from apps.seasons.utils.current import get_current_season

    try:
        season = get_current_season()
    except Exception:
        # No season row (or DB hiccup): don't hide otherwise-released content.
        return True
    return bool(season and season.new_features_on)


def visible_skills():
    """Queryset of skills a normal mortal is allowed to see on the public site,
    mirroring the game's ``mort_only`` predicate (ishar-mud info.c:8415-8436):
    a Skill / Spell / Passive that some playable class or race can currently
    learn, minus skills gated to a not-yet-live season. Immortal-only, mob-only,
    craft, enchant, deprecated, and unreleased skills are all excluded.
    """
    from apps.skills.models import Skill

    qs = Skill.objects.filter(
        skill_type__in=VISIBLE_SKILL_TYPES,
        skill_name__isnull=False,
        id__in=learnable_skill_ids(),
    )
    if not _new_features_on():
        qs = qs.exclude(enum_symbol__in=SEASON_GATED_ENUM_SYMBOLS)
    return qs


def find_skill_by_name(query: str):
    """Resolve a term to a mortal-visible Skill the way the game's
    ``is_skill_name`` does: an exact (case-insensitive) name, else an
    abbreviation (name prefix). Restricted to ``visible_skills()`` so the help
    fallback and direct URLs never surface a skill players shouldn't see.
    Returns a ``Skill`` or ``None``.
    """
    query = (query or "").strip()
    if not query:
        return None

    visible = visible_skills()
    exact = visible.filter(skill_name__iexact=query).first()
    if exact is not None:
        return exact

    # Abbreviation: the query is a prefix of the skill name (isabbrstring).
    return (
        visible.filter(skill_name__istartswith=query)
        .order_by("skill_name")
        .first()
    )
