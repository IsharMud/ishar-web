from datetime import datetime
from django.shortcuts import get_object_or_404
from ninja import Schema
from typing import List

from ishar.api import api
from ishar.apps.accounts.models import Account


class AccountSchema(Schema):
    """Account schema."""
    account_id: int
    account_name: str
    created_at: datetime
    last_login: datetime
    current_essence: int
    earned_essence: int
    seasonal_earned: int
    player_count: int


class AccountPlayersSchema(Schema):
    """Account players schema."""
    id: int
    name: str
    player_type: str


@api.get(
    path="/account/{name}/",
    response=AccountSchema,
    tags=["accounts"]
)
def account(request, name: str):
    """Single account, by name."""
    return get_object_or_404(Account, account_name=name)


@api.get(
    path="/account/{name}/players/",
    response=List[AccountPlayersSchema],
    tags=["accounts"]
)
def account_players(request, name: str):
    """Players related to a single account name."""
    return get_object_or_404(Account, account_name=name).players.all()


@api.get(path="/accounts/", response=List[AccountSchema], tags=["accounts"])
def accounts(request):
    """All accounts."""
    return Account.objects.all()
