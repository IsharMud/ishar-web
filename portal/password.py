
"""Portal, and pages for logged-in users"""
from flask import flash, render_template
from flask_login import current_user

from forms import ChangePasswordForm


def change_password():
    """Allow users to change their password"""

    # Get change password form object and check if submitted
    change_password_form = ChangePasswordForm()
    if change_password_form.validate_on_submit():

        # Proceed if the user entered their current password correctly
        verify = change_password_form.current_password.data
        new_choice = change_password_form.confirm_new_password.data
        if current_user.check_password(verify):
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
