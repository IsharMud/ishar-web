"""Dump the skill list as JSON, for curating the HUD's standardized icon map.

The skill names live only in the shared game database, so this read-only command
is how we get an offline list to build ``apps/connect/skill_icons.py`` from::

    python manage.py dump_skills > /tmp/skills.json

Then feed that JSON to the scratchpad ``build-skill-icons.js`` generator (which
applies the same keyword heuristic as ``hud.js``) to produce a starter
``id → icon`` map, hand-tune the misses, and paste it into ``skill_icons.py``.
See the 2026-07-16 design decision.
"""
import json

from django.core.management.base import BaseCommand

from apps.skills.models import Skill


class Command(BaseCommand):
    help = "Dump skills (id, enum_symbol, name, type) as JSON for icon-map curation."

    def handle(self, *args, **options):
        rows = [
            {
                "id": skill.pk,
                "enum_symbol": skill.enum_symbol,
                "name": skill.skill_name or "",
                "type": skill.type_name,   # "Skill" / "Spell" / "Craft" / ...
            }
            for skill in Skill.objects.all().order_by("id")
        ]
        self.stdout.write(json.dumps(rows, indent=2, ensure_ascii=False))
