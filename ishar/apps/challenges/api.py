from datetime import datetime
from django.shortcuts import get_object_or_404
from ninja import Schema
from typing import List

from ishar.api import api
from ishar.apps.challenges.models import Challenge


class ChallengeSchema(Schema):
    """Challenge schema."""
    challenge_id: int
    max_level: int
    max_people: int
    chall_tier: int
    challenge_desc: str
    winner_desc: str
    mob_name: str
    is_active: bool
    last_completion: datetime
    num_completed: int
    num_picked: int


@api.get(
    path="/challenge/{challenge_id}/",
    response=ChallengeSchema,
    tags=["challenges"]
)
def challenge(request, challenge_id: int):
    """Single challenge by ID."""
    return get_object_or_404(Challenge, challenge_id=challenge_id)


@api.get(
    path="/challenges/",
    response=List[ChallengeSchema],
    tags=["challenges"]
)
def challenges(request):
    """Any and all challenges - including inactive, incomplete, etc."""
    return Challenge.objects.all()


@api.get(
    path="/challenges/complete/",
    response=List[ChallengeSchema],
    tags=["challenges"]
)
def complete(request):
    """Active challenges with winners."""
    return Challenge.objects.filter(
        is_active__exact=1
    ).exclude(
        winner_desc__exact=""
    )


@api.get(
    path="/challenges/incomplete/",
    response=List[ChallengeSchema],
    tags=["challenges"]
)
def incomplete(request):
    """Active challenges, with NO winners."""
    return Challenge.objects.filter(
        is_active__exact=1,
        winner_desc__exact=""
    )


@api.get(
    path="/challenges/active/",
    response=List[ChallengeSchema],
    tags=["challenges"]
)
def active(request):
    """Challenges which are currently active."""
    return Challenge.objects.filter(is_active__exact=1)


@api.get(
    path="/challenges/inactive/",
    response=List[ChallengeSchema],
    tags=["challenges"]
)
def inactive(request):
    """Challenges which are currently NOT active."""
    return Challenge.objects.filter(is_active__exact=0)
