"""Frequently Asked Questions"""
from flask import Blueprint, render_template
from mud_secret import IMM_LEVELS
from models import Player

wizlist = Blueprint('wizlist', __name__)

@wizlist.route('/wiz_list/', methods=['GET'])
@wizlist.route('/wizlist/', methods=['GET'])
@wizlist.route('/wiz_list', methods=['GET'])
@wizlist.route('/wizlist', methods=['GET'])
def index():
    """Wizlist showing Immortals through Gods"""
    immortals = Player.query.filter(Player.true_level >= min(IMM_LEVELS)).order_by(-Player.true_level).all()
    return render_template('wizlist.html.j2', immortals=immortals)
