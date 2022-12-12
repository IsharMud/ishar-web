"""Portal, and pages for logged-in users"""
from flask import abort, Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from .forms import ChangePasswordForm, PlayerSearchForm
from .models import Player

# Flask Blueprint
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


@portal.route('/player/<string:player_name>/', methods=['GET', 'POST'])
@portal.route('/player/<string:player_name>', methods=['GET', 'POST'])
def player(player_name=None):
    """Player page to show detailed information about a player
        along with player name searching"""

    # Get player search form object and check if submitted
    find = None
    player_search_form = PlayerSearchForm()
    if player_search_form.validate_on_submit():

        # Perform a MySQL "LIKE" search query on the name,
        #   followed by a wildcard (%) to try to find the player
        find = Player.query.filter(
            Player.name.like(
                player_search_form.player_search_name.data + '%'
            )
        ).first()
        if find:
            who = find.name
        else:
            who = player_search_form.player_search_name.data

        return redirect(
            url_for(
                'portal.player',
                player_name=who,
                _anchor='player'
            )
        )

    # Find the player, in the database, by exact name
    if player_name:
        find = Player.query.filter_by(
            name=player_name
        ).first()

    # If our search returned something, we found a player
    if find:
        code = 200
    else:
        code = 404
        flash(
            'Sorry, but that player was not found!',
            'error'
        )

    return render_template(
        'player.html.j2',
        player=find,
        player_search_form=player_search_form
    ), code
