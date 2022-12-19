"""World"""
from flask import Blueprint, render_template

from help.helptab import search_help_topics


# Flask Blueprint
world_bp = Blueprint('world', __name__)


@world_bp.route('/areas/', methods=['GET'])
@world_bp.route('/areas', methods=['GET'])
@world_bp.route('/world/', methods=['GET'])
@world_bp.route('/world', methods=['GET'])
def index():
    """World page"""
    # Return only the areas from the helptab file
    return render_template(
        'world.html.j2',
        areas=search_help_topics(
            search='Area '
        )
    )
