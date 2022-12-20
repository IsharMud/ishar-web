"""View Player Profile"""
from flask import flash, redirect, render_template, url_for

from forms import PlayerSearchForm
from models import Player


def view_player(player_name=None):
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
                f'{player_search_form.player_search_name.data}%'
            )
        ).first()
        if find:
            who = find.name
        else:
            who = player_search_form.player_search_name.data

        return redirect(
            url_for(
                '.view_player',
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
