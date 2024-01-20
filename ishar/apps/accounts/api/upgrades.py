from typing import List

from django.shortcuts import get_object_or_404

from ishar.api import api
from ishar.apps.accounts.models import Account
from ishar.apps.accounts.models.upgrade import (
    AccountUpgrade, AccountAccountUpgrade
)
from ishar.apps.accounts.api.schemas import (
    AccountUpgradeSchema, AccountAccountUpgradeSchema
)


@api.get(
    path="/accounts/upgrades/",
    response=List[AccountUpgradeSchema],
    summary="Any and all available account upgrades.",
    tags=["accounts", "upgrades"]
)
def upgrades(request):
    """All account upgrades."""
    return AccountUpgrade.objects.all()


@api.get(
    path="/account/id/{account_id}/upgrades/",
    response=List[AccountAccountUpgradeSchema],
    summary="Upgrades related to a single account ID.",
    tags=["accounts", "upgrades"]
)
def account_id_upgrades(request, account_id: int):
    """Upgrades related to a single account ID."""
    return AccountAccountUpgrade.objects.filter(
        account_id=account_id,
        amount__gt=0
    ).all()


@api.get(
    path="/account/name/{account_name}/upgrades/",
    response=List[AccountAccountUpgradeSchema],
    summary="Upgrades related to a single account name.",
    tags=["accounts", "upgrades"]
)
def account_name_upgrades(request, account_name: str):
    """Upgrades related to a single account name."""
    account = get_object_or_404(Account, account_name=account_name)
    return AccountAccountUpgrade.objects.filter(
        account_id=account.account_id,
        amount__gt=0
    ).all()
