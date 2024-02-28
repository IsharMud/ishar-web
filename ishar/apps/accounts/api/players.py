from typing import List

from django.shortcuts import get_object_or_404

from ishar.apps.core.api import api
from ishar.apps.accounts.models import Account
from ishar.apps.accounts.api.schemas import AccountPlayerSchema


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
