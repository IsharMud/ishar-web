"""Leaders"""
from flask import Blueprint, render_template

from mud_secret import IMM_LEVELS
from models import Player


# Flask Blueprints
leaders_bp = Blueprint(
    'leaders',
    __name__,
    url_prefix='/leaders',
    template_folder='templates'
)
leaderboard_bp = Blueprint(
    'leaderboard',
    __name__,
    url_prefix='/leaderboard',
    template_folder='templates'
)


@leaders_bp.route('/', methods=['GET'])
@leaderboard_bp.route('/', methods=['GET'])
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


@leaders_bp.route('/classic/', methods=['GET'])
@leaders_bp.route('/classic', methods=['GET'])
@leaderboard_bp.route('/classic/', methods=['GET'])
@leaderboard_bp.route('/classic', methods=['GET'])
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


@leaders_bp.route('/survival/', methods=['GET'])
@leaders_bp.route('/survival', methods=['GET'])
@leaderboard_bp.route('/survival/', methods=['GET'])
@leaderboard_bp.route('/survival', methods=['GET'])
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
