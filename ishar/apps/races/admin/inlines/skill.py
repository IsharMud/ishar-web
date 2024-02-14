from ishar.apps.races.models.skill import RaceSkill

from . import BaseRaceAdminInline


class RaceSkillAdminInline(BaseRaceAdminInline):
    """Race skill inline administration."""
    model = RaceSkill
