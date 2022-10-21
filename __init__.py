"""
ishar_web
https://isharmud.com/
https://github.com/IsharMud/ishar-web
"""
from datetime import datetime, timedelta
import glob
import ipaddress
import os
from urllib.parse import urlparse
from flask import Flask, abort, current_app, flash, redirect, render_template, request, \
    session, url_for
from flask_login import current_user, fresh_login_required, login_required, login_user, \
    logout_user, LoginManager
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from database import db_session
from models import Account, Challenge, News, Player, PlayersFlag, PlayerQuest, \
    PlayerRemortUpgrade, Season
from mud_secret import PODIR, IMM_LEVELS
import forms
import helptab
import mud_clients

# Sentry
sentry_sdk.init(
    environment         = os.getenv('USER'),
    traces_sample_rate  = 1.0,
    integrations        = [FlaskIntegration(), SqlalchemyIntegration()],
    send_default_pii    = True
)

# Flask
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Flask-Login
login_manager                                   = LoginManager(app)
login_manager.login_message_category            = 'error'
login_manager.login_view                        = 'login'
login_manager.needs_refresh_message             = 'To protect your account, please log in again.'
login_manager.needs_refresh_message_category    = 'error'
login_manager.refresh_view                      = 'login'
login_manager.session_protection                = 'strong'

@login_manager.user_loader
def load_user(email):
    """Use Account database object for flask-login, via unique e-mail address"""
    user_account    = Account.query.filter_by(email = email).first()
    sentry_user     = None
    if user_account:
        sentry_user     = {
            'id'            : user_account.account_id,
            'username'      : user_account.account_name,
            'email'         : user_account.email,
            'essence'       : user_account.seasonal_points,
            'ip_address'    : request.remote_addr,
        }
    sentry_sdk.set_user(sentry_user)
    return user_account


@app.context_processor
def injects():
    """Add context processor for certain variables on all pages"""
    return dict(
        current_season  = get_current_season(),
        sentry_js       = get_sentry_js()
    )


def error(title='Unknown Error', message='Sorry, but there was an unknown error.', code=500):
    """Error template"""
    return render_template('error.html.j2', title=title, message=message), code

@app.errorhandler(400)
def bad_request(message):
    """Error codes to template above"""
    return error(title='Bad Request', message=message, code=400)

@app.errorhandler(401)
def not_authorized(message):
    """Error codes to template above"""
    sentry_sdk.capture_message(message, level='error')
    return error(title='Not Authorized', message=message, code=401)

@app.errorhandler(403)
def forbidden(message):
    """Error codes to template above"""
    sentry_sdk.capture_message(message, level='error')
    return error(title='Forbidden', message=message, code=403)

@app.errorhandler(404)
def page_not_found(message):
    """Error codes to template above"""
    return error(title='Page Not Found', message=message, code=404)

@app.errorhandler(500)
def internal_server_error(message):
    """Error codes to template above"""
    sentry_sdk.capture_message(message, level='error')
    return error(title='Internal Server Error', message=message, code=500)


def get_current_season():
    """Method to return the current season"""
    return Season.query.filter_by(is_active = 1).order_by(-Season.season_id).first()


def get_sentry_js(sentry_js=None):
    """Method to return the Sentry JavaScript SDK URI based on environment secret"""
    sentry_dsn  = os.getenv('SENTRY_DSN')
    if sentry_dsn:
        sentry_uri  = urlparse(sentry_dsn)
        if sentry_uri.username and sentry_uri.username != '':
            sentry_js   = f'https://js.sentry-cdn.com/{sentry_uri.username}.min.js'
    return sentry_js


@app.route('/welcome', methods=['GET'])
@app.route('/', methods=['GET'])
def welcome():
    """Main welcome page/index, includes the most recent news"""
    news    = News.query.order_by(-News.created_at).first()
    return render_template('welcome.html.j2', news=news)


@app.route('/background', methods=['GET'])
@app.route('/history', methods=['GET'])
def history():
    """History page mostly copied from the old website"""
    return render_template('history.html.j2')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log-in form page and processing"""

    # Get log in form object and check if submitted
    login_form = forms.LoginForm()
    if login_form.validate_on_submit():

        # Find the user by e-mail address from the log in form
        find = Account.query.filter_by(email = login_form.email.data).first()

        # If we find the user email and match the password, it is a successful log in
        if find is not None and find.check_password(login_form.password.data):
            flash('You have logged in!', 'success')
            login_user(find, remember=login_form.remember.data)

        # There must have been invalid credentials
        else:
            flash('Sorry, but please enter a valid e-mail address and password.', 'error')

    # Redirect authenticated users to the portal
    if current_user.is_authenticated:
        return redirect(session['next'] or url_for('portal'))

    # Show the log in form
    return render_template('login.html.j2', login_form=login_form), 401


@app.route('/season', methods=['GET'])
def season():
    """Information about the current season"""
    return render_template('season.html.j2', season=get_current_season())


@app.route('/password', methods=['GET', 'POST'])
@fresh_login_required
def change_password():
    """Allow logged in users to change their password"""

    # Get change password form object and check if submitted
    change_password_form = forms.ChangePasswordForm()
    if change_password_form.validate_on_submit():

        # Proceed if the user entered their current password correctly
        if current_user.check_password(change_password_form.current_password.data):
            if current_user.change_password(change_password_form.confirm_new_password.data):
                flash('Your password has been changed!', 'success')
            else:
                flash('Sorry, but your password could not be changed.', 'error')

        # Otherwise, tell them to enter their current password correctly
        else:
            flash('Please enter your current password correctly!', 'error')

    # Show the change password form
    return render_template('change_password.html.j2', change_password_form=change_password_form)


@app.route('/player/<string:player_name>', methods=['GET', 'POST'])
@login_required
def show_player(player_name=None):
    """Player page to show detailed information about a player
    along with player name searching"""

    # Get player search form object and check if submitted
    player  = None
    player_search_form  = forms.PlayerSearchForm()
    if player_search_form.validate_on_submit():

        # Perform a MySQL "LIKE" search query on the name,
        # followed by a wildcard (%) to try to find the player
        player  = Player.query.filter(
                    Player.name.like(
                        player_search_form.player_search_name.data + '%'
                    )
                ).first()
        if player:
            who = player.name
        else:
            who = player_search_form.player_search_name.data

        return redirect(url_for('show_player', player_name=who))

    # Find the player, in the database, by exact name
    if player_name:
        player  = Player.query.filter_by(name = player_name).first()

    # If our search returned something, we found a player
    if player:
        code    = 200
    else:
        code    = 404
        flash('Sorry, but that player was not found!', 'error')

    return render_template('player.html.j2',
                                player              = player,
                                player_search_form  = player_search_form
                            ), code


@app.route('/portal', methods=['GET'])
@login_required
def portal():
    """Main portal page for players logging in"""
    return render_template('portal.html.j2')


@app.route('/challenges', methods=['GET'])
def challenges():
    """Sort and list active challenges, along with their tiers and winners"""
    find    = Challenge.query.filter_by(is_active = 1).order_by(
                Challenge.adj_level,
                Challenge.adj_people
            ).all()
    return render_template('challenges.html.j2', challenges=find)


@app.route('/leaderboard', methods=['GET'])
@app.route('/leaderboard/<int:limit>', methods=['GET'])
@app.route('/leaders/<int:limit>', methods=['GET'])
@app.route('/leaders', methods=['GET'])
def leaders(limit=10):
    """Sort and list the best players, with a limit option,
        and boolean to include/exclude dead characters"""

    limit_choices   = [5, 10, 15, 20]
    if limit not in limit_choices or limit > max(limit_choices):
        return redirect(url_for('leaders', limit=10))

    if request.args.get('dead') and request.args.get('dead') == 'false':
        include_dead    = False
        leader_players  = Player.query.filter(
                            Player.true_level < min(IMM_LEVELS),
                            Player.is_deleted != 1
                        ).order_by(
                            -Player.remorts,
                            -Player.total_renown,
                            -Player.quests_completed,
                            -Player.challenges_completed,
                            Player.deaths
                        ).limit(limit).all()
    else:
        include_dead    = True
        leader_players  = Player.query.filter(
                            Player.true_level < min(IMM_LEVELS),
                        ).order_by(
                            -Player.remorts,
                            -Player.total_renown,
                            -Player.quests_completed,
                            -Player.challenges_completed,
                            Player.deaths
                        ).limit(limit).all()

    return render_template('leaders.html.j2',
                            include_dead    = include_dead,
                            leader_players  = leader_players,
                            limit           = limit,
                            limit_choices   = limit_choices
                        )


@app.route('/wiz_list', methods=['GET'])
@app.route('/wizlist', methods=['GET'])
def wizlist():
    """Wizlist showing Immortals through Gods"""
    immortals   =   Player.query.filter(
                        Player.true_level >= min(IMM_LEVELS)
                    ).order_by(
                        -Player.true_level
                    ).all()
    return render_template('wizlist.html.j2', immortals=immortals)


@app.route('/account', methods=['GET'])
@login_required
def manage_account():
    """Allow users to view/manage their accounts"""
    return render_template('account.html.j2')


@app.route('/admin', methods=['GET', 'POST'])
@fresh_login_required
def admin_portal():
    """Administration portal main page for Gods"""

    # Only allow access to Gods
    if not current_user.is_god:
        flash('Sorry, but you are not godly enough!', 'error')
        abort(401)

    # Show the administration portal
    return render_template('admin/portal.html.j2')


@app.route('/admin/news', methods=['GET', 'POST'])
@fresh_login_required
def admin_news():
    """Administration portal to allow Gods to post news
    /admin/news"""

    # Get news add form and check if submitted
    news_add_form   = forms.NewsAddForm()
    if news_add_form.validate_on_submit():

        # Create the model for the new news post and add it to the database
        new_news    = News(
            account_id      = current_user.account_id,
            created_at      = datetime.utcnow(),
            subject         = news_add_form.subject.data,
            body            = news_add_form.body.data
        )
        db_session.add(new_news)
        db_session.commit()
        if new_news.news_id:
            flash('Your message has been posted!', 'success')
        else:
            flash('Sorry, but please try again!', 'error')

    # Show the form to add news in the administration portal
    return render_template('admin/news.html.j2', news_add_form=news_add_form)


@app.route('/admin/account/<int:manage_account_id>', methods=['GET'])
@fresh_login_required
def admin_account(manage_account_id=None):
    """Administration portal to allow Gods to view accounts
    /admin/account"""

    # Only allow access to Gods
    if not current_user.is_god:
        flash('Sorry, but you are not godly enough!', 'error')
        abort(401)

    return render_template('admin/account.html.j2',
        manage_account  = Account.query.filter_by(account_id = manage_account_id).first()
    )


@app.route('/admin/account/edit/<int:edit_account_id>', methods=['GET', 'POST'])
@fresh_login_required
def admin_edit_account(edit_account_id=None):
    """Administration portal to allow Gods to edit accounts
    /admin/account/edit"""

    # Only allow access to Gods
    if not current_user.is_god:
        flash('Sorry, but you are not godly enough!', 'error')
        abort(401)

    edit_account    = Account.query.filter_by(account_id = edit_account_id).first()

    # Get edit account form and check if submitted
    edit_account_form   = forms.EditAccountForm()
    if edit_account_form.validate_on_submit():
        edit_account.account_name       = edit_account_form.account_name.data
        edit_account.email              = edit_account_form.email.data
        edit_account.seasonal_points    = edit_account_form.seasonal_points.data
        if edit_account_form.password.data != '' and edit_account_form.confirm_password.data != '':
            edit_account.change_password(edit_account_form.confirm_password.data)
            if edit_account.change_password(edit_account_form.confirm_password.data):
                flash('The account password was reset.', 'success')
                sentry_sdk.capture_message('Admin Password Reset: ' \
                    f'{current_user} reset {edit_account}', level='warning')
            else:
                flash('The account password could not be reset.', 'error')
                sentry_sdk.capture_message('Admin Password Reset Fail: ' \
                    f'{current_user} failed to reset {edit_account}', level='error')

        db_session.commit()
        flash('The account was updated successfully.', 'success')
        sentry_sdk.capture_message(f'Admin Edit Account: {current_user} edited {edit_account}')

    return render_template('admin/edit_account.html.j2',
                            edit_account        = edit_account,
                            edit_account_form   = edit_account_form
                        )


@app.route('/admin/accounts', methods=['GET'])
@fresh_login_required
def admin_accounts():
    """Administration portal to allow Gods to view accounts
    /admin/accounts"""

    # Only allow access to Gods
    if not current_user.is_god:
        flash('Sorry, but you are not godly enough!', 'error')
        abort(401)

    accounts    = Account.query.order_by(Account.account_id).all()
    return render_template('admin/accounts.html.j2', accounts=accounts)


@app.route('/admin/season', methods=['GET'])
@fresh_login_required
def admin_season():
    """Administration portal to allow Gods to view/manage seasons
    /admin/season"""

    # Only allow access to Gods
    if not current_user.is_god:
        flash('Sorry, but you are not godly enough!', 'error')
        abort(401)

    # Get all seasons for admins
    seasons = Season.query.order_by(
                -Season.is_active,
                -Season.season_id
            ).all()
    return render_template('admin/season.html.j2', seasons=seasons)


@app.route('/admin/season/cycle', methods=['GET', 'POST'])
@fresh_login_required
def admin_season_cycle():
    """Administration portal to allow Gods to cycle seasons, while wiping players
    /admin/season/cycle"""

    # Only allow access to Gods
    if not current_user.is_god:
        flash('Sorry, but you are not godly enough!', 'error')
        abort(401)

    # Get season cycle form, and check if submitted
    season_cycle_form = forms.SeasonCycleForm()
    if season_cycle_form.validate_on_submit():

        # Expire any existing active seasons
        for active_season in Season.query.filter_by(is_active = 1).all():
            active_season.is_active         = 0
            active_season.expiration_date   = datetime.utcnow()
            flash(f'Season {active_season.season_id} expired.', 'success')
            sentry_sdk.capture_message(f'Season Expired: {active_season}')

        # Create the model for the new season for the database entry
        new_season  = Season(
            is_active       = 1,
            effective_date  = season_cycle_form.effective_date.data,
            expiration_date = season_cycle_form.expiration_date.data
        )
        db_session.add(new_season)

        # Loop through all accounts
        #   to apply essence, and delete mortal players
        total_rewarded_essence  = 0
        total_players_deleted   = 0
        for account in Account.query.filter().all():
            if account.seasonal_earned > 0:
                calculated_essence  = account.seasonal_points + account.seasonal_earned
                flash(f'Account "{account.account_name}" ({ account.account_id}) ' \
                    f'now has {calculated_essence} essence. ' \
                    f'({account.seasonal_points} existing + ' \
                    f'{account.seasonal_earned} earned)', 'success')
                account.seasonal_points = calculated_essence
                total_rewarded_essence  += calculated_essence
            else:
                flash(f'Account "{account.account_name}" ' \
                    f'({ account.account_id}) earned no essence', 'warning')

            for delete_player in account.players:
                if not delete_player.is_immortal:
                    delete_path = f'{PODIR}/{delete_player.name}'
                    if os.path.exists(delete_path):
                        os.remove(delete_path)
                        flash(f'Deleted <code>{delete_path}</code>.', 'success')
                    db_session.query(PlayersFlag).filter_by(
                        player_id = delete_player.id).delete()
                    db_session.query(PlayerQuest).filter_by(
                        player_id = delete_player.id).delete()
                    db_session.query(PlayerRemortUpgrade).filter_by(
                        player_id = delete_player.id).delete()
                    db_session.query(Player).filter_by(
                        id = delete_player.id).delete()
                    flash(f'Deleted Player: {delete_player.name} ' \
                        f'({delete_player.id}).', 'success')
                    total_players_deleted   += 1
                else:
                    flash(f'Skipping immortal {delete_player.name}.', 'info')

        db_session.commit()
        flash('All essence has been rewarded.', 'success')
        flash(f'Total Rewarded Essence: {total_rewarded_essence} essence', 'info')
        sentry_sdk.capture_message(f'Essence Rewarded: {total_rewarded_essence} essence')

        if new_season.season_id:
            flash(f'Season {new_season.season_id} created.', 'success')
            sentry_sdk.capture_message(f'Season Created: {new_season}')

        find_players    = Player.query.filter(
                            Player.true_level < min(IMM_LEVELS)
                        ).all()
        if not find_players:
            flash('All mortal players have been deleted.', 'success')
            flash(f'Total Players Deleted: {total_players_deleted}', 'info')
            sentry_sdk.capture_message('Player Wipe: ' \
                f'{total_players_deleted} mortals deleted', level='warning')

    # Show the form to cycle a season in the administration portal
    return render_template('admin/season_cycle.html.j2', season_cycle_form=season_cycle_form)


@app.route('/logout', methods=['GET'])
def logout():
    """Allow users to log out (/logout)"""
    logout_user()
    flash('You have logged out!', 'success')
    sentry_sdk.set_user(None)
    return redirect(url_for('welcome'))


@app.route('/mud_clients', methods=['GET'])
@app.route('/clients', methods=['GET'])
def clients():
    """Page showing a dynamic list of various MUD clients for different platforms
        /clients (or /mud_clients)"""
    return render_template('clients.html.j2', clients=mud_clients.clients)


@app.route('/connect', methods=['GET'])
def connect():
    """Redirect /connect GET requests to mudslinger.net web client"""
    return redirect('https://mudslinger.net/play/?host=isharmud.com&port=23')


@app.route('/discord', methods=['GET'])
def discord():
    """Redirect /discord GET requests to the Discord invitation link"""
    return redirect('https://discord.gg/VBmMXUpeve')


@app.route('/latest_patch', methods=['GET'])
def latest_patch():
    """Redirect /latest_patch latest found static patch .pdf file"""
    return redirect('/' + max(glob.glob('static/patches/*.pdf'), key=os.path.getmtime))


@app.route('/patches/', methods=['GET'])
@app.route('/patches', methods=['GET'])
def patches():
    """Page showing a dynamic list of patches (/patches)"""
    return render_template('patches.html.j2',
                            patches = sorted(os.listdir('static/patches'), reverse=True)
                        )


@app.route('/questions')
@app.route('/faqs')
@app.route('/faq')
def faq():
    """A few frequently asked questions (/faq, /faqs, or /questions)"""
    import faqs
    return render_template('faq.html.j2', faqs=faqs.faqs)


@app.route('/gettingstarted')
@app.route('/getting_started')
@app.route('/getstarted')
@app.route('/get_started')
def get_started():
    """Get Started page partly copied from the old website"""
    return render_template('get_started.html.j2')


@app.route('/donate', methods=['GET'])
@app.route('/support', methods=['GET'])
def support():
    """Support page"""
    return render_template('support.html.j2')


@app.route('/areas/<string:area>', methods=['GET'])
@app.route('/areas', methods=['GET'])
@app.route('/world/<string:area>', methods=['GET'])
@app.route('/world', methods=['GET'])
def world(area=None):
    """World page that uses the game's existing helptab file
        to display information about each in-game area"""

    # Get all of the areas from the helptab file
    areas   = helptab.get_help_areas()
    code    = 200

    # Try to find an area based on any user input
    if area:
        if area in areas.keys():
            areas   = areas[area]
        else:
            area    = None
            code    = 404
            flash('Sorry, but please choose a valid area!', 'error')

    return render_template('world.html.j2', areas=areas, area=area), code


@app.route('/debug-sentry')
def trigger_error():
    """Trigger error for Sentry"""
    return 1 / 0


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Remove database session at request teardown
        and capture any exceptions"""
    if exception:
        sentry_sdk.capture_exception(exception)
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=True)
