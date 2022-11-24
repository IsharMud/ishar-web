"""Get Started"""
from flask import Blueprint, render_template

get_started = Blueprint('get_started', __name__)

@get_started.route('/getting_started/', methods=['GET'])
@get_started.route('/getting_started', methods=['GET'])
@get_started.route('/start/', methods=['GET'])
@get_started.route('/start', methods=['GET'])
@get_started.route('/get_started/', methods=['GET'])
@get_started.route('/get_started', methods=['GET'])
def index():
    """Get Started page"""
    return render_template('get_started.html.j2')
