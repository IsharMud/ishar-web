"""Leaders"""
from flask import Blueprint, render_template
from models import Player
from mud_secret import IMM_LEVELS

leaders = Blueprint('leaders', __name__)

@leaders.route('/leaderboard/', methods=['GET'])
@leaders.route('/leaders/', methods=['GET'])
@leaders.route('/leaderboard', methods=['GET'])
@leaders.route('/leaders', methods=['GET'])
def index():
    """Sort and list the best players"""
    leader_players = Player.query.filter(Player.true_level < min(IMM_LEVELS)).order_by(
        -Player.remorts,
        -Player.total_renown,
        -Player.quests_completed,
        -Player.challenges_completed,
        Player.deaths
    ).all()
    return render_template('leaders.html.j2', leader_players=leader_players)
