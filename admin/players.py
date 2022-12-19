"""Admin Players"""
from flask import abort, Blueprint, flash, render_template
from flask_login import current_user

from database import db_session
from forms import EditPlayerForm
from models import Player
from sentry import sentry_sdk


# Flask Blueprint
players = Blueprint(
    'players',
    __name__,
    url_prefix='/players',
    template_folder='templates/accounts'
)


@players.route('/edit/<int:edit_player_id>/', methods=['GET', 'POST'])
@players.route('/edit/<int:edit_player_id>', methods=['GET', 'POST'])
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
        player.money = edit_player_form.money.data
        player.align = edit_player_form.align.data
        player.karma = edit_player_form.karma.data
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
