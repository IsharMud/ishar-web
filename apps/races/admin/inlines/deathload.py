from ...models.deathload import RaceDeathload

from . import BaseRaceAdminInline


class RaceDeathloadAdminInline(BaseRaceAdminInline):
    """Race deathload inline administration."""

    model = RaceDeathload
