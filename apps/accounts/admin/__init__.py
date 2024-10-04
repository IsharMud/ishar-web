from django.contrib.admin import site

from ..models.account import Account
from ..models.upgrade import AccountUpgrade

from .account import AccountAdmin
from .upgrade import AccountUpgradeAdmin


site.register(Account, AccountAdmin)
site.register(AccountUpgrade, AccountUpgradeAdmin)
