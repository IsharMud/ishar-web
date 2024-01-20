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
    path="/account/{id_or_name}/",
    response=AccountSchema,
    tags=["accounts"]
)
def account(request, id_or_name):
    """Single account, by ID or name."""
    if id_or_name.isnumeric():
        return get_object_or_404(Account, account_id=id_or_name)
    return get_object_or_404(Account, account_name=id_or_name)


@api.get(
    path="/account/{id_or_name}/players/",
    response=List[AccountPlayersSchema],
    tags=["accounts"]
)
def account_players(request, id_or_name):
    """Players related to a single account, by ID or name."""
    if id_or_name.isnumeric():
        acct = get_object_or_404(Account, account_id=id_or_name)
    else:
        acct = get_object_or_404(Account, account_name=id_or_name)
    if acct.pk:
        return acct.players.all()
    return acct


@api.get(path="/accounts/", response=List[AccountSchema], tags=["accounts"])
def accounts(request):
    """All accounts."""
    return Account.objects.all()
