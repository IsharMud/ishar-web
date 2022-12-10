"""
ishar_web
https://isharmud.com/
https://github.com/IsharMud/ishar-web
"""
import os
from urllib.parse import urlparse

from flask import Flask
from login import login, login_manager

from admin import admin
from challenges import challenges
from database import db_session
from faqs import faqs
from get_started import get_started
from help_page import help_page
from history import history
from leaders import leaders
from models import Season
from mud_clients import mud_clients
from patches import patches
from players import players
from portal import portal
from redirects import redirects
from season import season
from sentry import sentry_sdk
from support import support
from wizlist import wizlist
from welcome import welcome
import error_pages

# Flask
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Error pages/handlers
app.register_blueprint(error_pages.error_pages)
app.register_error_handler(400, error_pages.bad_request)
app.register_error_handler(401, error_pages.not_authorized)
app.register_error_handler(403, error_pages.forbidden)
app.register_error_handler(404, error_pages.page_not_found)
app.register_error_handler(500, error_pages.internal_server_error)

# Flask-Login/Blueprints/pages
login_manager.init_app(app)
app.register_blueprint(admin)
app.register_blueprint(challenges)
app.register_blueprint(faqs)
app.register_blueprint(get_started)
app.register_blueprint(help_page)
app.register_blueprint(history)
app.register_blueprint(leaders)
app.register_blueprint(login)
app.register_blueprint(mud_clients)
app.register_blueprint(patches)
app.register_blueprint(players)
app.register_blueprint(portal)
app.register_blueprint(redirects)
app.register_blueprint(season)
app.register_blueprint(support)
app.register_blueprint(welcome)
app.register_blueprint(wizlist)


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
        sentry_dsn=sentry_dsn,
        sentry_user=sentry_uri.username,
        sentry_event_id=sentry_sdk.last_event_id()
    )


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Remove database session at request teardown and capture any exceptions"""
    if exception:
        sentry_sdk.capture_exception(exception)
    db_session.remove()


if __name__ == '__main__':
    app.run()
