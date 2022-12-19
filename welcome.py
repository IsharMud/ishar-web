"""Main page and pages accessible to all"""
from flask import Blueprint, redirect, render_template

from mud_secret import IMM_LEVELS
from models import GlobalEvent, News, Player


# Flask Blueprint
welcome_bp = Blueprint('welcome', __name__)


@welcome_bp.route('/background/', methods=['GET'])
@welcome_bp.route('/history/', methods=['GET'])
@welcome_bp.route('/background', methods=['GET'])
@welcome_bp.route('/history', methods=['GET'])
def history():
    """History/background page, mostly copied from original ishar.com"""
    return render_template('history.html.j2')


@welcome_bp.route('/global_events/', methods=['GET'])
@welcome_bp.route('/global_events', methods=['GET'])
@welcome_bp.route('/globalevents/', methods=['GET'])
@welcome_bp.route('/globalevents', methods=['GET'])
@welcome_bp.route('/events/', methods=['GET'])
@welcome_bp.route('/events', methods=['GET'])
def global_events():
    """List any global events"""
    return render_template(
        'global_events.html.j2',
        global_events=GlobalEvent.query.all()
    )


@welcome_bp.route('/connect/', methods=['GET'])
@welcome_bp.route('/connect', methods=['GET'])
def connect():
    """Redirect /connect GET requests to mudslinger.net web client"""
    return redirect(
        'https://mudslinger.net/play/?host=isharmud.com&port=23'
    )


@welcome_bp.route('/discord/invitation/', methods=['GET'])
@welcome_bp.route('/discord/invitation', methods=['GET'])
@welcome_bp.route('/discord/invite/', methods=['GET'])
@welcome_bp.route('/discord/invite', methods=['GET'])
@welcome_bp.route('/discord/', methods=['GET'])
@welcome_bp.route('/discord', methods=['GET'])
def discord_invite():
    """Redirect /discord GET requests to the Discord invite"""
    return redirect(
        'https://discord.gg/VBmMXUpeve'
    )


@welcome_bp.route('/start/', methods=['GET'])
@welcome_bp.route('/start', methods=['GET'])
@welcome_bp.route('/getting_started/', methods=['GET'])
@welcome_bp.route('/getting_started', methods=['GET'])
@welcome_bp.route('/gettingstarted/', methods=['GET'])
@welcome_bp.route('/gettingstarted', methods=['GET'])
@welcome_bp.route('/get_started/', methods=['GET'])
@welcome_bp.route('/get_started', methods=['GET'])
@welcome_bp.route('/getstarted/', methods=['GET'])
@welcome_bp.route('/getstarted', methods=['GET'])
def getstarted():
    """Get Started page"""
    return render_template('get_started.html.j2')


@welcome_bp.route('/season/', methods=['GET'])
@welcome_bp.route('/season', methods=['GET'])
def season():
    """Information about the current season"""
    return render_template('season.html.j2')


@welcome_bp.route('/donate/', methods=['GET'])
@welcome_bp.route('/donate', methods=['GET'])
@welcome_bp.route('/support/', methods=['GET'])
@welcome_bp.route('/support', methods=['GET'])
def support():
    """Support page"""
    return render_template('support.html.j2')


@welcome_bp.route('/welcome/', methods=['GET'])
@welcome_bp.route('/welcome', methods=['GET'])
@welcome_bp.route('/', methods=['GET'])
def index():
    """Main welcome page/index, includes the most recent news"""
    return render_template(
        'base/welcome.html.j2',
        news=News.query.order_by(
            -News.created_at
        ).first()
    )


@welcome_bp.route('/wiz_list/', methods=['GET'])
@welcome_bp.route('/wizlist/', methods=['GET'])
@welcome_bp.route('/wiz_list', methods=['GET'])
@welcome_bp.route('/wizlist', methods=['GET'])
def wizlist():
    """Wizlist showing Immortals through Gods"""
    return render_template(
        'wizlist.html.j2',
        immortals=Player.query.filter(
            Player.true_level >= min(IMM_LEVELS)
        ).order_by(
            -Player.true_level
        ).all()
    )
