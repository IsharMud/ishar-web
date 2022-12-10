"""Support"""
from flask import Blueprint, render_template

support = Blueprint('support', __name__)


@support.route('/donate/', methods=['GET'])
@support.route('/support/', methods=['GET'])
@support.route('/donate', methods=['GET'])
@support.route('/support', methods=['GET'])
def index():
    """Support page"""
    return render_template('support.html.j2')
