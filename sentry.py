"""Sentry"""
import os

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from config import SENTRY_DSN


sentry_sdk.init(
    dsn=SENTRY_DSN, environment=os.getenv('USER'),
    _experiments={'profiles_sample_rate': 1.0},
    integrations=[FlaskIntegration(), SqlalchemyIntegration()],
    release=os.getenv('USER'), send_default_pii=True, traces_sample_rate=1.0
)
