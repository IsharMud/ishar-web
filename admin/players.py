"""Admin Players"""
from flask import abort, Blueprint, flash, render_template
from flask_login import current_user, fresh_login_required

from database import db_session
from forms import EditPlayerForm
from models.player import Player
from sentry import sentry_sdk


# Flask Blueprint
admin_players_bp = Blueprint(
    'admin_players',
    __name__,
    url_prefix='players',
    template_folder='templates/accounts'
)


@admin_players_bp.before_request
@fresh_login_required
def before_request():
    """Only Gods can access /admin/players"""
    if not current_user.is_god:
        flash('Sorry, but you are not godly enough (Gods only)!', 'error')
        abort(401)


@admin_players_bp.route('/edit/<int:edit_player_id>/', methods=['GET', 'POST'])
@admin_players_bp.route('/edit/<int:edit_player_id>', methods=['GET', 'POST'])
def edit(edit_player_id=None):
    """Administration portal to allow Gods to edit player characters
        /admin/accounts/players/edit"""
    player = Player.query.filter_by(id=edit_player_id).first()

    if not player:
        flash('Invalid player.', 'error')
        abort(400)

    # Get edit player form and check if submitted
    edit_player_form = EditPlayerForm()
    if edit_player_form.validate_on_submit():
        player.name = edit_player_form.name.data
        player.common.alignment = edit_player_form.alignment.data
        player.common.gold = edit_player_form.gold.data
        player.common.karma = edit_player_form.karma.data
        player.renown = edit_player_form.renown.data
        player.is_deleted = edit_player_form.is_deleted.data
        db_session.commit()
        flash('The player was updated successfully.', 'success')
        sentry_sdk.capture_message(
            f'Admin Edit Player: {current_user} edited {player}'
        )

    return render_template(
        'edit_player.html.j2',
        edit_player=player,
        edit_player_form=edit_player_form
    )
