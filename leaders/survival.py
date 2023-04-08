"""Survival Leaders"""
from flask import render_template

from config import IMM_LEVELS
from models import Player


def survival():
    """Sort and list the best survival players"""
    return render_template(
        'leaders.html.j2',
        leader_players=Player.query.filter_by(
            game_type=1
        ).filter(
            Player.true_level < min(IMM_LEVELS)
        ).order_by(
            -Player.remorts,
            -Player.total_renown,
            -Player.quests_completed,
            -Player.challenges_completed,
            Player.deaths
        ).all()
    )
