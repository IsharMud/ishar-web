"""Portal, and pages for logged-in users"""
from flask import Blueprint, render_template

from models import News

welcome = Blueprint('welcome', __name__)


@welcome.route('/welcome/', methods=['GET'])
@welcome.route('/welcome', methods=['GET'])
@welcome.route('/', methods=['GET'])
def index():
    """Main welcome page/index, includes the most recent news"""
    return render_template(
        'welcome.html.j2',
        news=News.query.order_by(
            -News.created_at
        ).first()
    )
