"""
Ishar MUD API configuration.
"""
from django.conf import settings
from ninja import NinjaAPI


api = NinjaAPI(
    csrf=False,
    description=f"{settings.WEBSITE_TITLE} API",
    docs_url="/",
    title=settings.WEBSITE_TITLE
)

from ishar.apps.accounts.api import account, accounts
from ishar.apps.challenges.api import (
    challenge, challenges, incomplete_challenges, complete_challenges
)

