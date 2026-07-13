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


def find_skill_by_name(query: str):
    """Resolve a term to a Skill the way the game's ``is_skill_name`` does:
    an exact (case-insensitive) name, else an abbreviation (name prefix) across
    all skills — known or not. Returns a ``Skill`` or ``None``.
    """
    # Imported lazily to avoid a model/util import cycle.
    from apps.skills.models import Skill

    query = (query or "").strip()
    if not query:
        return None

    exact = Skill.objects.filter(skill_name__iexact=query).first()
    if exact is not None:
        return exact

    # Abbreviation: the query is a prefix of the skill name (isabbrstring).
    return (
        Skill.objects.filter(skill_name__istartswith=query)
        .order_by("skill_name")
        .first()
    )
