"""
ishar_web
https://isharmud.com/
https://github.com/IsharMud/ishar-web
"""
import os
from urllib.parse import urlparse
from flask import Flask

from error_pages import error_pages_bp
from login import login_bp, login_manager
from sentry import sentry_sdk
from database import db_session
from admin import admin_bp
from challenges import challenges_bp
from help import help_bp
from leaders import leaders_bp, leaderboard_bp
from patches import patches_bp
from portal import portal_bp
from sysinfo import sysinfo_bp
from welcome import welcome_bp
from models import GlobalEvent, Season


# Flask
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Error pages/handlers
app.register_blueprint(error_pages_bp)

# Flask-Login
login_manager.init_app(app)

# Flask Blueprints/pages
app.register_blueprint(admin_bp)
app.register_blueprint(challenges_bp)
app.register_blueprint(help_bp)
app.register_blueprint(leaders_bp)
app.register_blueprint(leaderboard_bp)
app.register_blueprint(login_bp)
app.register_blueprint(patches_bp)
app.register_blueprint(portal_bp)
app.register_blueprint(sysinfo_bp)
app.register_blueprint(welcome_bp)


@app.context_processor
def injects():
    """Add context processor for certain variables on all pages"""
    sentry_dsn = os.getenv('SENTRY_DSN')
    sentry_uri = urlparse(sentry_dsn)
    return {
        'current_season': Season.query.filter_by(is_active=1).order_by(
            -Season.season_id
        ).first(),
        'global_event_count': GlobalEvent.query.count(),
        'sentry_dsn': sentry_dsn,
        'sentry_user': sentry_uri.username,
        'sentry_event_id': sentry_sdk.last_event_id()
    }


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Remove database session at request teardown,
        and capture any exceptions"""
    if exception:
        sentry_sdk.capture_exception(exception)
    db_session.remove()


if __name__ == '__main__':
    app.run()
