"""Leaders"""
from flask import Blueprint, render_template

from config import IMM_LEVELS
from models import Player

from leaders.classic import classic
from leaders.survival import survival


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


@leaders_bp.route('/all/', methods=['GET'])
@leaders_bp.route('/all', methods=['GET'])
@leaders_bp.route('/', methods=['GET'])
@leaderboard_bp.route('/all/', methods=['GET'])
@leaderboard_bp.route('/all', methods=['GET'])
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


# Classic
leaders_bp.add_url_rule('/classic/', 'classic', classic, methods=['GET'])
leaders_bp.add_url_rule('/classic', 'classic', classic, methods=['GET'])
leaderboard_bp.add_url_rule('/classic/', 'classic', classic, methods=['GET'])
leaderboard_bp.add_url_rule('/classic', 'classic', classic, methods=['GET'])

# Survival
leaders_bp.add_url_rule('/survival/', 'survival', survival, methods=['GET'])
leaders_bp.add_url_rule('/survival', 'survival', survival, methods=['GET'])
leaderboard_bp.add_url_rule('/survival/', 'survival', survival, methods=['GET'])
leaderboard_bp.add_url_rule('/survival', 'survival', survival, methods=['GET'])
