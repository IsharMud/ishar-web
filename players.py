"""Player page"""
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required
from forms import PlayerSearchForm
from models import Player

players = Blueprint('players', __name__)

@players.route('/player/<string:player_name>/', methods=['GET', 'POST'])
@players.route('/player/<string:player_name>', methods=['GET', 'POST'])
@login_required
def view(player_name=None):
    """Player page to show detailed information about a player
        along with player name searching"""

    # Get player search form object and check if submitted
    player = None
    player_search_form = PlayerSearchForm()
    if player_search_form.validate_on_submit():

        # Perform a MySQL "LIKE" search query on the name,
        #   followed by a wildcard (%) to try to find the player
        player = Player.query.filter(Player.name.like(player_search_form.player_search_name.data + '%')).first()
        if player:
            who = player.name
        else:
            who = player_search_form.player_search_name.data

        return redirect(url_for('players.view', player_name=who, _anchor='player'))

    # Find the player, in the database, by exact name
    if player_name:
        player = Player.query.filter_by(name=player_name).first()

    # If our search returned something, we found a player
    if player:
        code = 200
    else:
        code = 404
        flash('Sorry, but that player was not found!', 'error')

    return render_template('player.html.j2', player=player, player_search_form=player_search_form), code
