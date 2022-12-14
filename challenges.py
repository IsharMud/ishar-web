"""Challenges"""
from flask import Blueprint, render_template

from models import Challenge


# Flask Blueprint
challenges = Blueprint('challenges', __name__)


@challenges.route('/challenges/all/', methods=['GET'])
@challenges.route('/challenges/all', methods=['GET'])
@challenges.route('/challenges/', methods=['GET'])
@challenges.route('/challenges', methods=['GET'])
def index():
    """Sort and list active challenges, along with their tiers and winners"""
    return render_template(
        'challenges.html.j2',
        challenges=Challenge.query.filter_by(
            is_active=1
        ).order_by(
            Challenge.adj_level,
            Challenge.adj_people
        ).all()
    )


@challenges.route('/challenges/done/', methods=['GET'])
@challenges.route('/challenges/done', methods=['GET'])
@challenges.route('/challenges/complete/', methods=['GET'])
@challenges.route('/challenges/complete', methods=['GET'])
@challenges.route('/challenges/completed/', methods=['GET'])
@challenges.route('/challenges/completed', methods=['GET'])
def complete():
    """Sort and list completed challenges, along with their tiers and winners"""
    return render_template(
        'challenges.html.j2',
        challenges=Challenge.query.filter_by(
            is_active=1).filter(
                Challenge.winner_desc != ''
            ).order_by(
                Challenge.adj_level,
                Challenge.adj_people
        ).all()
    )


@challenges.route('/challenges/todo/', methods=['GET'])
@challenges.route('/challenges/todo', methods=['GET'])
@challenges.route('/challenges/incomplete/', methods=['GET'])
@challenges.route('/challenges/incomplete', methods=['GET'])
def incomplete():
    """Sort and list completed challenges, along with their tiers and winners"""
    return render_template(
        'challenges.html.j2',
        challenges=Challenge.query.filter_by(
            is_active=1).filter(
                Challenge.winner_desc != ''
            ).order_by(
                Challenge.adj_level,
                Challenge.adj_people
        ).all()
    )
