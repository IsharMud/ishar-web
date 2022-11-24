"""Admin"""
import os
from datetime import datetime
from functools import wraps
from flask import abort, Blueprint, flash, render_template
from flask_login import current_user, fresh_login_required
import sentry_sdk
from database import db_session
from forms import EditAccountForm, EditPlayerForm, NewsAddForm, SeasonCycleForm
from models import Account, News, Player, Season
from mud_secret import PODIR, IMM_LEVELS


def god_required(func):
    """Decorator to allow access only to Gods"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_god:
            flash('Sorry, but you are not godly enough!', 'error')
            abort(401)
        return func(*args, **kwargs)
    return decorated_function


admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/', methods=['GET', 'POST'])
@fresh_login_required
@god_required
def index():
    """Administration portal main page for Gods"""
    return render_template('admin/portal.html.j2')


@admin.route('/news', methods=['GET', 'POST'])
@fresh_login_required
@god_required
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
            flash('Your message has been posted!', 'success')
        else:
            flash('Sorry, but please try again!', 'error')

    # Show the form to add news in the administration portal
    return render_template('admin/news.html.j2', news_add_form=news_add_form)


@admin.route('/account/<int:manage_account_id>', methods=['GET'])
@fresh_login_required
@god_required
def manage_account(manage_account_id=None):
    """Administration portal to allow Gods to view accounts
        /admin/account"""
    return render_template('admin/manage_account.html.j2',
                           manage_account=Account.query.filter_by(account_id=manage_account_id).first()
                           )


@admin.route('/account/edit/<int:edit_account_id>', methods=['GET', 'POST'])
@fresh_login_required
@god_required
def edit_account(edit_account_id=None):
    """Administration portal to allow Gods to edit accounts
        /admin/account/edit"""
    account = Account.query.filter_by(account_id=edit_account_id).first()

    # Get edit account form and check if submitted
    edit_account_form = EditAccountForm()
    if edit_account_form.validate_on_submit():
        account.account_name = edit_account_form.account_name.data
        account.email = edit_account_form.email.data
        account.seasonal_points = edit_account_form.seasonal_points.data
        if edit_account_form.password.data != '' and edit_account_form.confirm_password.data != '':
            account.change_password(edit_account_form.confirm_password.data)
            if account.change_password(edit_account_form.confirm_password.data):
                flash('The account password was reset.', 'success')
                sentry_sdk.capture_message('Admin Password Reset: '
                                           f'{current_user} reset {account}', level='warning')
            else:
                flash('The account password could not be reset.', 'error')
                sentry_sdk.capture_message('Admin Password Reset Fail: '
                                           f'{current_user} failed to reset {account}', level='error')

        db_session.commit()
        flash('The account was updated successfully.', 'success')
        sentry_sdk.capture_message(f'Admin Edit Account: {current_user} edited {account}')

    return render_template('admin/edit_account.html.j2',
                           edit_account=account,
                           edit_account_form=edit_account_form
                           )


@admin.route('/accounts', methods=['GET'])
@fresh_login_required
@god_required
def accounts():
    """Administration portal to allow Gods to view accounts
        /admin/accounts"""
    return render_template('admin/accounts.html.j2', accounts=Account.query.order_by(Account.account_id).all())


@admin.route('/player/edit/<int:edit_player_id>', methods=['GET', 'POST'])
@fresh_login_required
@god_required
def edit_player(edit_player_id=None):
    """Administration portal to allow Gods to edit player characters
        /admin/player/edit"""
    player = Player.query.filter_by(id=edit_player_id).first()

    # Get edit player form and check if submitted
    edit_player_form = EditPlayerForm()
    if edit_player_form.validate_on_submit():
        player.name = edit_player_form.name.data
        player.align = edit_player_form.align.data
        player.karma = edit_player_form.karma.data
        player.renown = edit_player_form.renown.data
        db_session.commit()
        flash('The player was updated successfully.', 'success')
        sentry_sdk.capture_message(f'Admin Edit Player: {current_user} edited {player}')

    return render_template('admin/edit_player.html.j2',
                           edit_player=player,
                           edit_player_form=edit_player_form
                           )


@admin.route('/season', methods=['GET'])
@fresh_login_required
@god_required
def season():
    """Administration portal to allow Gods to view/manage seasons
        /admin/season"""
    return render_template('admin/season.html.j2',
                           seasons=Season.query.order_by(-Season.is_active, -Season.season_id).all()
                           )


@admin.route('/season/cycle', methods=['GET', 'POST'])
@fresh_login_required
@god_required
def season_cycle():
    """Administration portal to allow Gods to cycle seasons, while wiping players
        /admin/season/cycle"""

    # Get season cycle form, and check if submitted
    season_cycle_form = SeasonCycleForm()
    if season_cycle_form.validate_on_submit():

        # Expire any existing active seasons
        for active_season in Season.query.filter_by(is_active=1).all():
            active_season.is_active = 0
            active_season.expiration_date = datetime.utcnow()
            flash(f'Season {active_season.season_id} expired.', 'success')
            sentry_sdk.capture_message(f'Season Expired: {active_season}')

        # Create the new season database entry
        new_season = Season(
            is_active=1,
            effective_date=season_cycle_form.effective_date.data,
            expiration_date=season_cycle_form.expiration_date.data
        )
        db_session.add(new_season)

        # Loop through all accounts - to apply essence, and delete mortal players
        total_rewarded_essence = total_players_deleted = 0
        for account in Account.query.filter().all():
            if account.seasonal_earned > 0:
                calculated_essence = account.seasonal_points + account.seasonal_earned
                flash(f'Account "{account.account_name}" ({account.account_id}) '
                      f'now has {calculated_essence} essence. '
                      f'({account.seasonal_points} existing + '
                      f'{account.seasonal_earned} earned)', 'success')
                account.seasonal_points = calculated_essence
                total_rewarded_essence += calculated_essence
            else:
                flash(f'Account "{account.account_name}"'
                      f'({account.account_id}) earned no essence', 'warning')

            for delete_player in account.players:
                if not delete_player.is_immortal:
                    delete_path = PODIR + '/' + delete_player.name
                    if os.path.exists(delete_path):
                        os.remove(delete_path)
                        flash(f'Deleted <code>{delete_path}</code>.', 'success')
                    db_session.query(Player).filter_by(id=delete_player.id).delete()
                    flash(f'Deleted Player: {delete_player.name} ({delete_player.id}).', 'success')
                    total_players_deleted += 1
                else:
                    flash(f'Skipping immortal {delete_player.name}.', 'info')

        db_session.commit()
        flash('All essence has been rewarded.', 'success')
        flash(f'Total Rewarded Essence: {total_rewarded_essence} essence', 'info')
        sentry_sdk.capture_message(f'Essence Rewarded: {total_rewarded_essence} essence')

        if new_season.season_id:
            flash(f'Season {new_season.season_id} created.', 'success')
            sentry_sdk.capture_message(f'Season Created: {new_season}')

        if not Player.query.filter(Player.true_level < min(IMM_LEVELS)).all():
            flash('All mortal players have been deleted.', 'success')
            flash(f'Total Players Deleted: {total_players_deleted}', 'info')
            sentry_sdk.capture_message('Player Wipe: {total_players_deleted} mortals deleted', level='warning')

    # Show the form to cycle a season in the administration portal
    return render_template('admin/season_cycle.html.j2', season_cycle_form=season_cycle_form)
