"""Admin"""
from flask import abort, Blueprint, flash, render_template
from flask_login import current_user, fresh_login_required

from admin.accounts import admin_accounts_bp
from admin.events import admin_events_bp
from admin.news import admin_news_bp
from admin.patches import admin_patches_bp
from admin.quests import admin_quests_bp
from admin.seasons import admin_seasons_bp


# Flask Blueprints
admin_bp = Blueprint(
    'admin', __name__, url_prefix='admin', template_folder='templates'
)
admin_bp.register_blueprint(admin_accounts_bp)
admin_bp.register_blueprint(admin_events_bp)
admin_bp.register_blueprint(admin_news_bp)
admin_bp.register_blueprint(admin_patches_bp)
admin_bp.register_blueprint(admin_quests_bp)
admin_bp.register_blueprint(admin_seasons_bp)


@admin_bp.before_request
@fresh_login_required
def before_request():
    """Only Eternals and above can access /admin"""
    if not current_user.is_eternal:
        flash(
            'Sorry, but you are not godly enough (Eternals and above only)!',
            'error'
        )
        abort(401)


@admin_bp.route('/', methods=['GET'])
def index():
    """Administration portal main page for Gods"""
    return render_template('portal.html.j2')
