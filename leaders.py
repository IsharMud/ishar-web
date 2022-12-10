"""Leaders"""
from flask import Blueprint, render_template

from mud_secret import IMM_LEVELS
from models import Player

leaders = Blueprint('leaders', __name__)


@leaders.route('/leaderboard/all/', methods=['GET'])
@leaders.route('/leaders/all/', methods=['GET'])
@leaders.route('/leaderboard/all', methods=['GET'])
@leaders.route('/leaders/all', methods=['GET'])
@leaders.route('/leaderboard/', methods=['GET'])
@leaders.route('/leaders/', methods=['GET'])
@leaders.route('/leaderboard', methods=['GET'])
@leaders.route('/leaders', methods=['GET'])
def index():
    """Sort and list the best players"""
    return render_template(
        'leaders.html.j2',
        leader_players=Player.query.filter(
            Player.true_level < min(IMM_LEVELS)
        ).order_by(
            -Player.remorts,
            -Player.total_renown,
            -Player.quests_completed,
            -Player.challenges_completed,
            Player.deaths
        ).all()
    )


@leaders.route('/leaderboard/classic/', methods=['GET'])
@leaders.route('/leaders/classic/', methods=['GET'])
@leaders.route('/leaderboard/classic', methods=['GET'])
@leaders.route('/leaders/classic', methods=['GET'])
def classic():
    """Sort and list the best classic players"""
    return render_template(
        'leaders.html.j2',
        leader_players=Player.query.filter_by(game_type=0).filter(
            Player.true_level < min(IMM_LEVELS)
        ).order_by(
            -Player.remorts,
            -Player.total_renown,
            -Player.quests_completed,
            -Player.challenges_completed,
            Player.deaths
        ).all()
    )


@leaders.route('/leaderboard/survival/', methods=['GET'])
@leaders.route('/leaders/survival/', methods=['GET'])
@leaders.route('/leaderboard/survival', methods=['GET'])
@leaders.route('/leaders/survival', methods=['GET'])
def survival():
    """Sort and list the best survival players"""
    return render_template(
        'leaders.html.j2',
        leader_players=Player.query.filter_by(game_type=1).filter(
            Player.true_level < min(IMM_LEVELS)
        ).order_by(
            -Player.remorts,
            -Player.total_renown,
            -Player.quests_completed,
            -Player.challenges_completed,
            Player.deaths
        ).all()
    )
