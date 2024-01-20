from typing import List

from django.shortcuts import get_object_or_404

from ishar.api import api
from ishar.apps.accounts.models import Account
from ishar.apps.accounts.api.schemas import AccountSchema


@api.get(
    path="/accounts/",
    response=List[AccountSchema],
    summary="Any and all accounts.",
    tags=["accounts"]
)
def accounts(request):
    """All accounts."""
    return Account.objects.all()


@api.get(
    path="/account/id/{account_id}/",
    response=AccountSchema,
    summary="Single account, by ID.",
    tags=["accounts"]
)
def account_id(request, account_id: int):
    """Single account, by ID."""
    return get_object_or_404(Account, account_id=account_id)


@api.get(
    path="/account/name/{account_name}/",
    response=AccountSchema,
    summary="Single account, by name.",
    tags=["accounts"]
)
def account_name(request, account_name: str):
    """Single account, by name."""
    return get_object_or_404(Account, account_name=account_name)
