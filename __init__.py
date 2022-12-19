"""
ishar_web
https://isharmud.com/
https://github.com/IsharMud/ishar-web
"""
import os
from urllib.parse import urlparse

from flask import Flask
from login import login, login_manager
from sentry import sentry_sdk
from database import db_session
from admin import admin
from challenges import challenges
from faqs import faqs
from help_page import help_page
from leaders import leaders, leaderboard
from mud_clients import mud_clients
from patches import patches
from portal import portal
from sysinfo import sysinfo
from welcome import welcome

from error_pages import error_pages
from models import GlobalEvent, Season


# Flask
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Error pages/handlers
app.register_blueprint(error_pages)

# Flask-Login
login_manager.init_app(app)

# Flask Blueprints/pages
app.register_blueprint(admin)
app.register_blueprint(challenges)
app.register_blueprint(faqs)
app.register_blueprint(help_page)
app.register_blueprint(leaders)
app.register_blueprint(leaderboard)
app.register_blueprint(login)
app.register_blueprint(mud_clients)
app.register_blueprint(patches)
app.register_blueprint(portal)
app.register_blueprint(sysinfo)
app.register_blueprint(welcome)


@app.context_processor
def injects():
    """Add context processor for certain variables on all pages"""
    sentry_dsn = os.getenv('SENTRY_DSN')
    sentry_uri = urlparse(sentry_dsn)
    return dict(
        current_season=Season.query.filter_by(
            is_active=1
        ).order_by(
            -Season.season_id
        ).first(),
        global_event_count=GlobalEvent.query.count(),
        sentry_dsn=sentry_dsn,
        sentry_user=sentry_uri.username,
        sentry_event_id=sentry_sdk.last_event_id()
    )


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Remove database session at request teardown,
        and capture any exceptions"""
    if exception:
        sentry_sdk.capture_exception(exception)
    db_session.remove()


if __name__ == '__main__':
    app.run()
