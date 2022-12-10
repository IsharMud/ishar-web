"""Portal, and pages for logged-in users"""
from flask import abort, Blueprint, flash, render_template
from flask_login import current_user, login_required

from forms import ChangePasswordForm

portal = Blueprint('portal', __name__)


@portal.before_request
@login_required
def before_request():
    """Only logged-in users"""
    if not current_user.is_authenticated:
        abort(401)


@portal.route('/portal/', methods=['GET'])
@portal.route('/portal', methods=['GET'])
def index():
    """Main portal page for logged-in players"""
    return render_template('portal.html.j2')


@portal.route('/essence/', methods=['GET'])
@portal.route('/essence', methods=['GET'])
@portal.route('/account/', methods=['GET'])
@portal.route('/account', methods=['GET'])
def account():
    """Allow users to view/manage their accounts"""
    return render_template('account.html.j2')


@portal.route('/password/', methods=['GET', 'POST'])
@portal.route('/password', methods=['GET', 'POST'])
def change_password():
    """Allow users to change their password"""

    # Get change password form object and check if submitted
    change_password_form = ChangePasswordForm()
    if change_password_form.validate_on_submit():

        # Proceed if the user entered their current password correctly
        verify_existing = change_password_form.current_password.data
        new_choice = change_password_form.confirm_new_password.data
        if current_user.check_password(verify_existing):
            if current_user.change_password(new_choice):
                flash(
                    'Your password has been changed!',
                    'success'
                )
            else:
                flash(
                    'Sorry, but your password could not be changed.',
                    'error'
                )

        # Otherwise, tell them to enter their current password correctly
        else:
            flash(
                'Please enter your current password correctly!',
                'error'
            )

    # Show the change password form
    return render_template(
        'change_password.html.j2',
        change_password_form=change_password_form
    )
