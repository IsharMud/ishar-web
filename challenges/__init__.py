"""Challenges"""
from flask import Blueprint, render_template

from models import Challenge


# Flask Blueprint
challenges = Blueprint(
    'challenges',
    __name__,
    url_prefix='/challenges',
    template_folder='templates'
)


@challenges.route('/all/', methods=['GET'])
@challenges.route('/all', methods=['GET'])
@challenges.route('/', methods=['GET'])
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


@challenges.route('/done/', methods=['GET'])
@challenges.route('/done', methods=['GET'])
@challenges.route('/complete/', methods=['GET'])
@challenges.route('/complete', methods=['GET'])
@challenges.route('/completed/', methods=['GET'])
@challenges.route('/completed', methods=['GET'])
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


@challenges.route('/todo/', methods=['GET'])
@challenges.route('/todo', methods=['GET'])
@challenges.route('/incomplete/', methods=['GET'])
@challenges.route('/incomplete', methods=['GET'])
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
