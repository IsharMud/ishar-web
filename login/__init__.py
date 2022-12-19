"""Log-in page/form and Flask-Login """
from flask import Blueprint, flash, redirect, render_template, request, \
    session, url_for
from flask_login import current_user, login_user, logout_user, LoginManager

from forms import LoginForm
from models import Account
from sentry import sentry_sdk


# Flask-Login
login_manager = LoginManager()
login_manager.login_message_category = 'error'
login_manager.login_view = 'login.player_login'
login_manager.needs_refresh_message = 'Please log in again, for your security.'
login_manager.needs_refresh_message_category = 'error'
login_manager.refresh_view = 'login.player_login'
login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(email):
    """Use Account database table for flask-login, via unique e-mail address"""
    user_account = Account.query.filter_by(email=email).first()
    if user_account:
        sentry_sdk.set_user({
            'id': user_account.account_id,
            'username': user_account.account_name,
            'email': user_account.email,
            'ip_address': request.remote_addr
        })
    return user_account


# Flask Blueprint
login_bp = Blueprint(
    'login',
    __name__,
    url_prefix='/',
    template_folder='templates'
)


@login_bp.route('/login/', methods=['GET', 'POST'])
@login_bp.route('/login', methods=['GET', 'POST'])
def player_login():
    """Log-in form page and processing"""

    # Get log in form object and check if submitted
    login_form = LoginForm()
    if login_form.validate_on_submit():

        # Find the user by e-mail address from the log-in form
        find = Account.query.filter_by(email=login_form.email.data).first()

        # If we find the user email and match the password,
        #   it is a successful log in
        if find and find.check_password(login_form.password.data):
            flash(
                'You have logged in!',
                'success'
            )
            login_user(
                user=find,
                remember=login_form.remember.data
            )

        # There must have been invalid credentials
        else:
            flash(
                'Sorry, but please enter a valid e-mail address and password.',
                'error'
            )

    # Redirect authenticated users to their requested page, or the portal
    if current_user.is_authenticated:
        try:
            return redirect(
                session['next']
            )
        except KeyError:
            return redirect(
                url_for('portal.index')
            )

    # Show the log-in form with 401 response
    return render_template(
        'login.html.j2',
        login_form=login_form
    ), 401


@login_bp.route('/logout/', methods=['GET'])
@login_bp.route('/logout', methods=['GET'])
def player_logout():
    """Allow users to log out (/logout)"""
    logout_user()
    flash(
        'You have logged out!',
        'success'
    )
    sentry_sdk.set_user(None)
    return redirect(
        url_for('welcome_bp.index')
    )
