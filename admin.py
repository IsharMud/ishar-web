"""Admin"""
import os
from datetime import datetime

from flask import abort, Blueprint, flash, render_template, url_for
from flask_login import current_user, fresh_login_required

from .mud_secret import PODIR, IMM_LEVELS
from .database import db_session
from .forms import EditAccountForm, EditPlayerForm, NewsAddForm, \
    PatchAddForm, SeasonCycleForm
from .models import Account, News, Player, Season
from .sentry import sentry_sdk


# Flask Blueprint
admin = Blueprint(
    'admin',
    __name__,
    url_prefix='/admin'
)


@admin.before_request
@fresh_login_required
def before_request():
    """Only Gods can access /admin"""
    if not current_user.is_god:
        flash('Sorry, but you are not godly enough!', 'error')
        abort(401)


def is_pdf(filename=None):
    """Check if file is a PDF, based on the file name"""
    ext = filename.rsplit('.', 1)[1].lower()
    print('ext:', ext)
    if ext == 'pdf':
        return True
    return False


@admin.route('/', methods=['GET', 'POST'])
def index():
    """Administration portal main page for Gods"""
    return render_template('admin/portal.html.j2')


@admin.route('/news/', methods=['GET', 'POST'])
@admin.route('/news', methods=['GET', 'POST'])
def news():
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
                'admin.edit_news',
                edit_news_id=new_news.news_id
            )
            flash(
                'Your message has been posted! '
                f'You can <a href="{edit_url}">edit it here</a>.',
                'success'
            )
        else:
            flash('Sorry, but please try again!', 'error')

    # Show the form to add news in the administration portal
    return render_template(
        'admin/news.html.j2',
        all_news=News.query.order_by(-News.created_at).all(),
        news_add_form=news_add_form
    )


@admin.route('/news/edit/<int:edit_news_id>/', methods=['GET', 'POST'])
@admin.route('/news/edit/<int:edit_news_id>', methods=['GET', 'POST'])
def edit_news(edit_news_id=None):
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
        'admin/edit_news.html.j2',
        edit_news=news_post,
        edit_news_form=edit_news_form
    )


@admin.route('/news/delete/<int:delete_news_id>/', methods=['GET'])
@admin.route('/news/delete/<int:delete_news_id>', methods=['GET'])
def delete_news(delete_news_id=None):
    """Administration portal to allow Gods to edit news posts
        /admin/news/edit"""
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

    # Show the form to add news in the administration portal
    return render_template(
        'admin/news.html.j2',
        all_news=News.query.order_by(-News.created_at).all(),
        news_add_form=NewsAddForm()
    )


@admin.route('/account/<int:manage_account_id>/', methods=['GET'])
@admin.route('/account/<int:manage_account_id>', methods=['GET'])
def manage_account(manage_account_id=None):
    """Administration portal to allow Gods to view accounts
        /admin/account"""
    account = Account.query.filter_by(account_id=manage_account_id).first()

    if not account:
        flash('Invalid account.', 'error')
        abort(400)

    return render_template(
        'admin/manage_account.html.j2',
        manage_account=account
    )


@admin.route('/account/edit/<int:edit_account_id>/', methods=['GET', 'POST'])
@admin.route('/account/edit/<int:edit_account_id>', methods=['GET', 'POST'])
def edit_account(edit_account_id=None):
    """Administration portal to allow Gods to edit accounts
        /admin/account/edit"""

    # Find the account based on the ID in the URL
    account = Account.query.filter_by(
        account_id=edit_account_id
    ).first()

    # 400 if bad account
    if not account:
        flash('Invalid account.', 'error')
        abort(400)

    # Get edit account form and check if submitted
    edit_account_form = EditAccountForm()
    if edit_account_form.validate_on_submit():

        # Update database with submitted form values
        account.account_name = edit_account_form.account_name.data
        account.email = edit_account_form.email.data
        account.seasonal_points = edit_account_form.seasonal_points.data

        # Process administrative password reset
        if edit_account_form.confirm_password.data:
            if account.change_password(
                new_password=edit_account_form.confirm_password.data
            ):
                flash(
                    f'The account ({account.name}) password was reset.',
                    'success'
                )
                sentry_sdk.capture_message(
                    'Admin Password Reset: '
                    f'{current_user} reset {account}'
                )
            else:
                flash(
                    'The account password could not be reset.',
                    'error'
                )
                sentry_sdk.capture_message(
                    'Admin Password Reset Fail: '
                    f'{current_user} failed to reset {account}',
                    level='error'
                )

        db_session.commit()
        flash('The account was updated successfully.', 'success')
        sentry_sdk.capture_message(
            'Admin Edit Account: '
            f'{current_user} edited {account}'
        )

    return render_template(
        'admin/edit_account.html.j2',
        edit_account=account,
        edit_account_form=edit_account_form
    )


@admin.route('/accounts/', methods=['GET'])
@admin.route('/accounts', methods=['GET'])
def accounts():
    """Administration portal to allow Gods to view accounts
        /admin/accounts"""
    return render_template(
        'admin/accounts.html.j2',
        accounts=Account.query.order_by(
            Account.account_id
        ).all()
    )


@admin.route('/player/edit/<int:edit_player_id>/', methods=['GET', 'POST'])
@admin.route('/player/edit/<int:edit_player_id>', methods=['GET', 'POST'])
def edit_player(edit_player_id=None):
    """Administration portal to allow Gods to edit player characters
        /admin/player/edit"""
    player = Player.query.filter_by(id=edit_player_id).first()

    if not player:
        flash('Invalid player.', 'error')
        abort(400)

    # Get edit player form and check if submitted
    edit_player_form = EditPlayerForm()
    if edit_player_form.validate_on_submit():
        player.name = edit_player_form.name.data
        player.money = edit_player_form.money.data
        player.align = edit_player_form.align.data
        player.karma = edit_player_form.karma.data
        player.renown = edit_player_form.renown.data
        player.is_deleted = edit_player_form.is_deleted.data
        db_session.commit()
        flash(
            'The player was updated successfully.',
            'success'
        )
        sentry_sdk.capture_message(
            'Admin Edit Player: '
            f'{current_user} edited {player}'
        )

    return render_template(
        'admin/edit_player.html.j2',
        edit_player=player,
        edit_player_form=edit_player_form
    )


@admin.route('/season/', methods=['GET'])
@admin.route('/season', methods=['GET'])
def season():
    """Administration portal to allow Gods to view/manage seasons
        /admin/season"""
    return render_template(
        'admin/season.html.j2',
        seasons=Season.query.order_by(
            -Season.is_active,
            -Season.season_id
        ).all()
    )


@admin.route('/season/cycle/', methods=['GET', 'POST'])
@admin.route('/season/cycle', methods=['GET', 'POST'])
def season_cycle():
    """Administration portal to allow Gods to cycle seasons,
        while wiping players - /admin/season/cycle"""

    # Get season cycle form, and check if submitted
    season_cycle_form = SeasonCycleForm()
    if season_cycle_form.validate_on_submit():

        # Expire any existing active seasons
        for active_season in Season.query.filter_by(is_active=1).all():
            active_season.is_active = 0
            active_season.expiration_date = datetime.utcnow()
            flash(
                f'Season {active_season.season_id} expired.',
                'success'
            )
            sentry_sdk.capture_message(
                f'Season Expired: {active_season}'
            )

        # Create the new season database entry
        new_season = Season(
            is_active=1,
            effective_date=season_cycle_form.effective_date.data,
            expiration_date=season_cycle_form.expiration_date.data
        )
        db_session.add(new_season)

        # Loop through all accounts
        total_rewarded_essence = total_players_deleted = 0
        for account in Account.query.filter().all():

            # Apply any essence earned
            if account.seasonal_earned > 0:

                # Add existing essence plus essence earned
                calculated_essence = f'{account.seasonal_points} ' \
                                     f'{account.seasonal_earned}'
                flash(
                    f'Account "{account.display_name}" '
                    f'({account.account_id}) '
                    f'now has {calculated_essence} essence. '
                    f'({account.seasonal_points} existing + '
                    f'{account.seasonal_earned} earned)',
                    'success'
                )

                # Update account essence balance in the database, and total
                account.seasonal_points = calculated_essence
                total_rewarded_essence += calculated_essence

            # Mention accounts that earned no essence
            else:
                flash(
                    f'Account "{account.display_name}" '
                    f'({account.account_id}) earned no essence',
                    'warning'
                )

            # Loop through each player in each account
            for delete_player in account.players:

                # Do not remove immortal players
                if not delete_player.is_immortal:

                    # Physically delete the Podir file for any mortal players
                    delete_path = PODIR + '/' + delete_player.name
                    if os.path.exists(delete_path):
                        os.remove(delete_path)
                        flash(
                            f'Deleted <code>{delete_path}</code>.',
                            'success'
                        )

                    # Delete mortal players from the database
                    do_delete = db_session.query(Player).filter_by(
                                    id=delete_player.id
                                ).delete()
                    if do_delete:
                        flash(
                            f'Deleted Player: {delete_player.name} '
                            f'({delete_player.id}).',
                            'success'
                        )
                        total_players_deleted += 1
                    else:
                        flash(
                            f'Delete Player Fail: {delete_player.name} '
                            f'({delete_player.id}).',
                            'error'
                        )
                        sentry_sdk.capture_message(
                            'Delete Player Fail: '
                            f'{delete_player.name} '
                            f'({delete_player.id})',
                            level='error'
                        )

        # Commit the changes to the database
        db_session.commit()
        flash('All essence has been rewarded.', 'success')
        flash(
            f'Total Rewarded Essence: {total_rewarded_essence} essence',
            'info'
        )
        sentry_sdk.capture_message(
            'Essence Rewarded: ',
            f'{total_rewarded_essence} essence'
        )

        # Make sure a season was created
        if new_season.season_id:
            flash(f'Season {new_season.season_id} created.', 'success')
            sentry_sdk.capture_message(
                f'Season Created: {new_season}'
            )

        # Make sure that only immortals remain
        if not Player.query.filter(Player.true_level < min(IMM_LEVELS)).all():
            flash(
                'All mortal players have been deleted.',
                'success'
            )
            flash(
                f'Total Players Deleted: {total_players_deleted}',
                'info'
            )
            sentry_sdk.capture_message(
                f'Player Wipe: {total_players_deleted} mortals deleted'
            )

    # Show the form to cycle a season in the administration portal
    return render_template(
        'admin/season_cycle.html.j2',
        season_cycle_form=season_cycle_form
    )


@admin.route('/patches/', methods=['GET', 'POST'])
@admin.route('/patches', methods=['GET', 'POST'])
def patches():
    """Administration portal to allow Gods to upload patch PDFs
        /admin/patches"""

    # Get patch add form and check if submitted
    patch_add_form = PatchAddForm()
    if patch_add_form.validate_on_submit():

        # WIP: Validate & upload file,
        #   probably split /admin/ into multiple files...
        #       (news, account, etc.)

        flash('Sorry, but this form is still being built!', 'error')

    # Show the form to add patches in the administration portal
    return render_template(
        'admin/patches.html.j2',
        all_patches=None,
        patch_add_form=patch_add_form
    )
