"""Help"""
from flask import Blueprint, render_template

from help.faqs import faqs_bp
from help.help_page import help_page_bp
from help.mud_clients import mud_clients_bp
from help.world import world_bp


# Flask Blueprints
help_bp = Blueprint(
    'help', __name__, url_prefix='/', template_folder='templates'
)
help_bp.register_blueprint(faqs_bp)
help_bp.register_blueprint(help_page_bp)
help_bp.register_blueprint(mud_clients_bp)
help_bp.register_blueprint(world_bp)


@help_bp.route('/background/', methods=['GET'])
@help_bp.route('/history/', methods=['GET'])
@help_bp.route('/background', methods=['GET'])
@help_bp.route('/history', methods=['GET'])
def history():
    """History/Background page (mostly copied from original ishar.com)"""
    return render_template('history.html.j2')


@help_bp.route('/start/', methods=['GET'])
@help_bp.route('/start', methods=['GET'])
@help_bp.route('/getting_started/', methods=['GET'])
@help_bp.route('/getting_started', methods=['GET'])
@help_bp.route('/gettingstarted/', methods=['GET'])
@help_bp.route('/gettingstarted', methods=['GET'])
@help_bp.route('/get_started/', methods=['GET'])
@help_bp.route('/get_started', methods=['GET'])
@help_bp.route('/getstarted/', methods=['GET'])
@help_bp.route('/getstarted', methods=['GET'])
def getstarted():
    """Get Started page"""
    return render_template('get_started.html.j2')
