"""Portal, and pages for logged in users"""
from flask import Blueprint, flash, redirect, render_template, session, url_for
from flask_login import current_user, fresh_login_required, login_required, login_user, logout_user
from forms import ChangePasswordForm, LoginForm
from models import Account
from sentry import sentry_sdk

portal = Blueprint('portal', __name__)


@portal.route('/portal/', methods=['GET'])
@portal.route('/portal', methods=['GET'])
@login_required
def index():
    """Main portal page for players logging in"""
    return render_template('portal.html.j2')


@portal.route('/login/', methods=['GET', 'POST'])
@portal.route('/login', methods=['GET', 'POST'])
def login():
    """Log-in form page and processing"""

    # Get log in form object and check if submitted
    login_form = LoginForm()
    if login_form.validate_on_submit():

        # Find the user by e-mail address from the log-in form
        find = Account.query.filter_by(email=login_form.email.data).first()

        # If we find the user email and match the password, it is a successful log in
        if find is not None and find.check_password(login_form.password.data):
            flash('You have logged in!', 'success')
            login_user(find, remember=login_form.remember.data)

        # There must have been invalid credentials
        else:
            flash('Sorry, but please enter a valid e-mail address and password.', 'error')

    # Redirect authenticated users to the portal
    if current_user.is_authenticated:
        return redirect(session['next'] or url_for('portal.index'))

    # Show the log-in form
    return render_template('login.html.j2', login_form=login_form), 401


@portal.route('/essence/', methods=['GET'])
@portal.route('/essence', methods=['GET'])
@portal.route('/account/', methods=['GET'])
@portal.route('/account', methods=['GET'])
@login_required
def account():
    """Allow users to view/manage their accounts"""
    return render_template('account.html.j2')


@portal.route('/logout/', methods=['GET'])
@portal.route('/logout', methods=['GET'])
def logout():
    """Allow users to log out (/logout)"""
    logout_user()
    flash('You have logged out!', 'success')
    sentry_sdk.set_user(None)
    return redirect(url_for('welcome'))


@portal.route('/password/', methods=['GET', 'POST'])
@portal.route('/password', methods=['GET', 'POST'])
@fresh_login_required
def change_password():
    """Allow users to change their password"""

    # Get change password form object and check if submitted
    change_password_form = ChangePasswordForm()
    if change_password_form.validate_on_submit():

        # Proceed if the user entered their current password correctly
        if current_user.check_password(change_password_form.current_password.data):
            if current_user.change_password(change_password_form.confirm_new_password.data):
                flash('Your password has been changed!', 'success')
            else:
                flash('Sorry, but your password could not be changed.', 'error')

        # Otherwise, tell them to enter their current password correctly
        else:
            flash('Please enter your current password correctly!', 'error')

    # Show the change password form
    return render_template('change_password.html.j2', change_password_form=change_password_form)
