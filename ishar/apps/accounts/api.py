from datetime import datetime
from django.shortcuts import get_object_or_404
from ninja import Schema
from typing import List

from ishar.api import api
from ishar.apps.accounts.models import Account


class AccountSchema(Schema):
    """Account API schema."""
    account_id: int
    created_at: datetime
    current_essence: int
    email: str
    account_name: str
    earned_essence: int


@api.get(path="/accounts", response=List[AccountSchema])
def accounts(request):
    qs = Account.objects
    if request.user.is_superuser():
        return qs.all()
    return qs.filter(account=request.user).all()


@api.get(path="/accounts/{account_id}", response=AccountSchema)
def account(request, account_id: int):
    account = get_object_or_404(Account, account_id=account_id)
    if not request.user == account or not request.user.is_superuser():
        return 401, {"message": ""}
    if request.user == account:
        return account
    return 401, {'message': 'Unauthorized'}
