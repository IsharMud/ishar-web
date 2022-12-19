"""Admin"""
from flask import abort, Blueprint, flash, render_template
from flask_login import current_user, fresh_login_required

from admin.accounts import admin_accounts
from admin.events import admin_events
from admin.news import admin_news
from admin.patches import admin_patches
from admin.seasons import admin_seasons


# Flask Blueprints
admin = Blueprint(
    'admin',
    __name__,
    url_prefix='/admin',
    template_folder='templates'
)
admin.register_blueprint(admin_accounts)
admin.register_blueprint(admin_events)
admin.register_blueprint(admin_news)
admin.register_blueprint(admin_patches)
admin.register_blueprint(admin_seasons)


@admin.before_request
@fresh_login_required
def before_request():
    """Only Gods can access /admin"""
    if not current_user.is_god:
        flash('Sorry, but you are not godly enough!', 'error')
        abort(401)


@admin.route('/', methods=['GET'])
def index():
    """Administration portal main page for Gods"""
    return render_template('portal.html.j2')
