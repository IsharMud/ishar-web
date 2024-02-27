from ...models.affinity import RaceAffinity

from . import BaseRaceAdminInline


class RaceAffinityAdminInline(BaseRaceAdminInline):
    """Race affinity inline administration."""
    model = RaceAffinity
