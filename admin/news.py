"""Admin News"""
from datetime import datetime

from flask import abort, Blueprint, flash, render_template, url_for
from flask_login import current_user, fresh_login_required

from database import db_session
from forms import NewsAddForm
from models.news import News
from sentry import sentry_sdk


# Flask Blueprint
admin_news_bp = Blueprint(
    'admin_news',
    __name__,
    url_prefix='/news',
    template_folder='templates/news'
)


@admin_news_bp.before_request
@fresh_login_required
def before_request():
    """Only Gods can access /admin/news"""
    if not current_user.is_god:
        flash('Sorry, but you are not godly enough (Gods only)!', 'error')
        abort(401)


@admin_news_bp.route('/', methods=['GET', 'POST'])
def index():
    """Administration portal to allow Gods to post news
        /admin/news"""

    # Get news add form and check if submitted
    news_add_form = NewsAddForm()
    if news_add_form.validate_on_submit():

        # Create the new news post database entry
        new_news = News(
            account_id=current_user.account_id,
            created_at=datetime.utcnow(),
            subject=news_add_form.subject.data,
            body=news_add_form.body.data
        )
        db_session.add(new_news)
        db_session.commit()
        if new_news.news_id:
            edit_url = url_for(
                '.edit',
                edit_news_id=new_news.news_id
            )
            flash(
                'Your message has been posted! '
                f'You can <a href="{edit_url}">edit it here</a>.',
                'success'
            )
        else:
            flash('Sorry, but please try again!', 'error')

    # Show the form to manage news in the administration portal
    return render_template(
        'news.html.j2',
        all_news=News.query.order_by(-News.created_at).all(),
        news_add_form=news_add_form
    )


@admin_news_bp.route('/edit/<int:edit_news_id>/', methods=['GET', 'POST'])
@admin_news_bp.route('/edit/<int:edit_news_id>', methods=['GET', 'POST'])
def edit(edit_news_id=None):
    """Administration portal to allow Gods to edit news posts
        /admin/news/edit"""
    news_post = News.query.filter_by(news_id=edit_news_id).first()
    if not news_post:
        flash('Invalid news post.', 'error')
        abort(400)

    # Get news form, and check if submitted
    edit_news_form = NewsAddForm()
    if edit_news_form.validate_on_submit():
        news_post.subject = edit_news_form.subject.data
        news_post.body = edit_news_form.body.data
        db_session.commit()
        flash('The news post was updated successfully.', 'success')
        sentry_sdk.capture_message(
            'Admin Edit News: '
            f'{current_user} edited {news_post}'
        )

    return render_template(
        'edit_news.html.j2',
        edit_news=news_post,
        edit_news_form=edit_news_form
    )


@admin_news_bp.route('/delete/<int:delete_news_id>/', methods=['GET'])
@admin_news_bp.route('/delete/<int:delete_news_id>', methods=['GET'])
def delete(delete_news_id=None):
    """Administration portal to allow Gods to delete news posts
        /admin/news/delete"""
    news_post = News.query.filter_by(news_id=delete_news_id).first()
    if not news_post:
        flash('Invalid news post.', 'error')
        abort(400)

    News.query.filter_by(news_id=news_post.news_id).delete()
    db_session.commit()
    flash('The news post was deleted successfully.', 'success')
    sentry_sdk.capture_message(
        'Admin Delete News: '
        f'{current_user} deleted {news_post}'
    )

    # Show the form to manage news in the administration portal
    return index()
