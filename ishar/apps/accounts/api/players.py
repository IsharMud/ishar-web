from datetime import datetime
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Schema

from ishar.api import api
from ishar.apps.accounts.models import Account


class AccountPlayerSchema(Schema):
    """Account player schema."""
    id: int
    name: str
    is_deleted: bool
    birth: datetime
    logon: datetime
    logout: datetime
    bankacc: int
    deaths: int
    remorts: int
    renown: int
    true_level: int
    favors: int
    total_renown: int
    quests_completed: int
    challenges_completed: int
    game_type: int
    player_stats: dict
    player_type: str


@api.get(
    path="/account/id/{account_id}/players/",
    response=List[AccountPlayerSchema],
    summary="Players related to a single account ID.",
    tags=["accounts", "players"]
)
def account_id_players(request, account_id: int):
    """Players related to a single account ID."""
    return get_object_or_404(Account, account_id=account_id).players.all()


@api.get(
    path="/account/name/{account_name}/players/",
    response=List[AccountPlayerSchema],
    summary="Players related to a single account name.",
    tags=["accounts", "players"]
)
def account_name_players(request, account_name: str):
    """Players related to a single account name."""
    return get_object_or_404(Account, account_name=account_name).players.all()
