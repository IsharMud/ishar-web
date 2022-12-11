"""Challenges"""
from flask import Blueprint, render_template

from models import Challenge

challenges = Blueprint('challenges', __name__)


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
