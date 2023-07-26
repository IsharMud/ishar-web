"""Portal, and pages for logged-in users"""
from flask import abort, Blueprint, render_template
from flask_login import current_user, login_required

from portal.password import change_password
from portal.players import view_player


# Flask Blueprint
portal_bp = Blueprint(
    'portal',
    __name__,
    url_prefix='/',
    template_folder='templates'
)


@portal_bp.before_request
@login_required
def before_request():
    """Only logged-in users"""
    if not current_user.is_authenticated:
        abort(401)


@portal_bp.route('/portal/', methods=['GET'])
def player_portal():
    """Main portal page for logged-in players"""
    return render_template('player_portal.html.j2')


@portal_bp.route('/essence/', methods=['GET'])
@portal_bp.route('/account/', methods=['GET'])
def account():
    """Allow users to view/manage their accounts"""
    return render_template('account.html.j2')


# Change password
portal_bp.add_url_rule(
    '/change_password/', 'change_password', change_password,
    methods=['GET', 'POST']
)
portal_bp.add_url_rule(
    '/change-password/', 'change_password', change_password,
    methods=['GET', 'POST']
)
portal_bp.add_url_rule(
    '/changepassword/', 'change_password', change_password,
    methods=['GET', 'POST']
)
portal_bp.add_url_rule(
    '/password/', 'change_password', change_password,
    methods=['GET', 'POST']
)

# View player
portal_bp.add_url_rule(
    '/player/<string:player_name>/', 'view_player', view_player,
    methods=['GET', 'POST']
)
