"""
ishar_web
https://isharmud.com/
https://github.com/IsharMud/ishar-web
"""
import os
from urllib.parse import urlparse
from flask import Flask, render_template, request
from flask_login import LoginManager
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from database import db_session
from models import Account, News, Season

from admin import admin
from challenges import challenges
from faqs import faqs
from get_started import get_started
from help_page import help_page
from history import history
from leaders import leaders
from mud_clients import mud_clients
from patches import patches
from players import players
from portal import portal
from redirects import redirects
from season import season
from support import support
from wizlist import wizlist
from world import world


# Sentry
sentry_sdk.init(
    environment=os.getenv('USER'),
    traces_sample_rate=1.0,
    integrations=[FlaskIntegration(), SqlalchemyIntegration()],
    send_default_pii=True,
    _experiments={
        "profiles_sample_rate": 1.0,
    }
)


# Flask
app = Flask(__name__)
app.config.from_pyfile('config.py')


# Flask Blueprints/pages
app.register_blueprint(admin)
app.register_blueprint(challenges)
app.register_blueprint(faqs)
app.register_blueprint(get_started)
app.register_blueprint(help_page)
app.register_blueprint(history)
app.register_blueprint(leaders)
app.register_blueprint(mud_clients)
app.register_blueprint(patches)
app.register_blueprint(players)
app.register_blueprint(portal)
app.register_blueprint(redirects)
app.register_blueprint(season)
app.register_blueprint(support)
app.register_blueprint(wizlist)
app.register_blueprint(world)


# Flask-Login
login_manager = LoginManager(app)
login_manager.login_message_category = 'error'
login_manager.login_view = 'portal.login'
login_manager.needs_refresh_message = 'To protect your account, please log in again.'
login_manager.needs_refresh_message_category = 'error'
login_manager.refresh_view = 'portal.login'
login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(email):
    """Use Account database object for flask-login, via unique e-mail address"""
    user_account = Account.query.filter_by(email=email).first()
    if user_account:
        sentry_sdk.set_user({
            'id': user_account.account_id,
            'username': user_account.account_name,
            'email': user_account.email,
            'ip_address': request.remote_addr
        })
    return user_account


@app.context_processor
def injects():
    """Add context processor for certain variables on all pages"""
    sentry_dsn = os.getenv('SENTRY_DSN')
    sentry_uri = urlparse(sentry_dsn)
    return dict(
        current_season=Season.query.filter_by(is_active=1).order_by(-Season.season_id).first(),
        sentry_dsn=sentry_dsn,
        sentry_user=sentry_uri.username,
        sentry_event_id=sentry_sdk.last_event_id()
    )


def error(title='Unknown Error', message='Sorry, but there was an unknown error.', code=500):
    """Error template"""
    return render_template('error.html.j2', title=title, message=message), code


@app.errorhandler(400)
def bad_request(message):
    """400 error"""
    return error(title='Bad Request', message=message, code=400)


@app.errorhandler(401)
def not_authorized(message):
    """401 error (with Sentry)"""
    sentry_sdk.capture_message(message, level='error')
    return error(title='Not Authorized', message=message, code=401)


@app.errorhandler(403)
def forbidden(message):
    """403 error (with Sentry)"""
    sentry_sdk.capture_message(message, level='error')
    return error(title='Forbidden', message=message, code=403)


@app.errorhandler(404)
def page_not_found(message):
    """404 error"""
    return error(title='Page Not Found', message=message, code=404)


@app.errorhandler(500)
def internal_server_error(message):
    """500 error (with Sentry)"""
    sentry_sdk.capture_message(message, level='error')
    return error(title='Internal Server Error', message=message, code=500)


@app.route('/welcome/', methods=['GET'])
@app.route('/welcome', methods=['GET'])
@app.route('/', methods=['GET'])
def welcome():
    """Main welcome page/index, includes the most recent news"""
    return render_template('welcome.html.j2', news=News.query.order_by(-News.created_at).first())


@app.route('/debug-sentry', methods=['GET'])
def trigger_error():
    """Trigger error for Sentry"""
    return 1 / 0


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Remove database session at request teardown and capture any exceptions"""
    if exception:
        sentry_sdk.capture_exception(exception)
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=True)
