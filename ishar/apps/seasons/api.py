from datetime import datetime
from django.shortcuts import get_object_or_404
from ninja import Schema
from typing import List

from ishar.api import api

from .models import Season
from .util import get_current_season


class SeasonSchema(Schema):
    """Season schema."""
    season_id: int
    is_active: bool
    effective_date: datetime
    expiration_date: datetime
    last_challenge_cycle: datetime


@api.get(
    path="/season/",
    response=SeasonSchema,
    summary="Current season.",
    tags=["seasons"]
)
def current(request):
    """Current season."""
    return Season.objects.get(season_id=get_current_season().season_id)


@api.get(
    path="/seasons/",
    response=List[SeasonSchema],
    summary="Any and all seasons.",
    tags=["seasons"]
)
def seasons(request):
    """All seasons."""
    return Season.objects.all()


@api.get(
    path="/season/{season_id}/",
    response=SeasonSchema,
    summary="Single season, by ID.",
    tags=["seasons"]
)
def season(request, season_id: int):
    """Single season, by ID."""
    return get_object_or_404(Season, season_id=season_id)
