"""Season"""
from flask import Blueprint, render_template

season = Blueprint('season', __name__)

@season.route('/season/', methods=['GET'])
@season.route('/season', methods=['GET'])
def index():
    """Information about the current season"""
    return render_template('season.html.j2')
