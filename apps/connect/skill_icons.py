"""Curated skill → game-icons mapping — the *standardized* icon set every
player of the web HUD inherits.

Keyed by the game's **stable skill id** (the ``id`` on the ``skills`` table and
in the ``Char.Skills`` GMCP feed), so it survives skill renames. Each icon name
must exist in ``apps/connect/static/img/game-icons.svg``.

Resolution order in the client (``hud.js`` ``iconName``):

    per-player pick  →  server-provided icon  →  THIS map  →  keyword heuristic

So this map overrides the client-side keyword heuristic but yields to a
player's personal choice and to a future authoritative ``icon`` field the game
may emit (see the 2026-07-16 design decision). Anything not listed here simply
falls through to the heuristic, so a partial map is fine — fill it in over time.

To (re)generate a starter map from the live skill table::

    python manage.py dump_skills > /tmp/skills.json

Then apply the ``hud.js`` keyword heuristic (``ICON_RULES``) to that dump to get
a starter ``id → icon`` mapping — an easy job to hand to Claude Code — review
the misses, and paste the entries below. Keep the ``# ENUM_SYMBOL — skill name``
comment on each line so the map stays human-editable.
"""

# id: "icon",   # ENUM_SYMBOL — skill name
SKILL_ICONS: dict[int, str] = {
}
