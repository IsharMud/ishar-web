"""Sentry"""
import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

sentry_sdk.init(
    environment=os.getenv('USER'),
    release=os.getenv('USER'),
    traces_sample_rate=1.0,
    integrations=[FlaskIntegration(), SqlalchemyIntegration()],
    send_default_pii=True,
    _experiments={
        'profiles_sample_rate': 1.0
    }
)
