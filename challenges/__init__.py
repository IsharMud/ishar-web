"""Challenges"""
from flask import Blueprint, render_template

from models.challenge import Challenge


# Flask Blueprint
challenges_bp = Blueprint(
    'challenges', __name__,
    url_prefix='/challenges',
    template_folder='templates'
)


@challenges_bp.route('/all/', methods=['GET'])
@challenges_bp.route('/', methods=['GET'])
def index():
    """Sort and list aLL active challenges,
        along with their tiers and winners"""
    return render_template(
        'challenges.html.j2',
        challenges=Challenge.query.filter_by(
            is_active=1
        ).order_by(
            Challenge.adj_level,
            Challenge.adj_people
        ).all()
    )


@challenges_bp.route('/done/', methods=['GET'])
@challenges_bp.route('/complete/', methods=['GET'])
@challenges_bp.route('/completed/', methods=['GET'])
def complete():
    """Sort and list completed challenges,
        along with their tiers and winners"""
    return render_template(
        'challenges.html.j2',
        challenges=Challenge.query.filter_by(
            is_active=1
        ).filter(
            Challenge.winner_desc != ''
        ).order_by(
            Challenge.adj_level,
            Challenge.adj_people
        ).all()
    )


@challenges_bp.route('/todo/', methods=['GET'])
@challenges_bp.route('/incomplete/', methods=['GET'])
def incomplete():
    """Sort and list incomplete challenges,
        along with their tiers and winners"""
    return render_template(
        'challenges.html.j2',
        challenges=Challenge.query.filter_by(
            is_active=1
        ).filter(
            Challenge.winner_desc == ''
        ).order_by(
            Challenge.adj_level,
            Challenge.adj_people
        ).all()
    )
