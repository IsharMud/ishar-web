"""History"""
from flask import Blueprint, render_template

history = Blueprint('history', __name__)


@history.route('/background/', methods=['GET'])
@history.route('/history/', methods=['GET'])
@history.route('/background', methods=['GET'])
@history.route('/history', methods=['GET'])
def index():
    """History page, mostly copied from original ishar.com"""
    return render_template('history.html.j2')
