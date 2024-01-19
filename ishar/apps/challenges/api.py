from datetime import datetime
from django.shortcuts import get_object_or_404
from ninja import Schema
from typing import List

from ishar.api import api
from ishar.apps.challenges.models import Challenge


class ChallengeSchema(Schema):
    """Challenge API schema."""
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


@api.get(path="/challenges", response=List[ChallengeSchema])
def challenges(request):
    return Challenge.objects.filter(is_active__exact=1)


@api.get(path="/challenges/complete", response=List[ChallengeSchema])
def complete_challenges(request):
    return Challenge.objects.filter(
        is_active__exact=1
    ).exclude(
        winner_desc__exact=""
    )


@api.get(path="/challenges/incomplete", response=List[ChallengeSchema])
def incomplete_challenges(request):
    return Challenge.objects.filter(
        is_active__exact=1,
        winner_desc__exact=""
    )


@api.get(path="/challenges/{challenge_id}", response=ChallengeSchema)
def challenge(request, challenge_id: int):
    return get_object_or_404(Challenge, challenge_id=challenge_id)

