import datetime
from flask import Flask, flash, redirect, render_template, request, send_from_directory, session, url_for
from flask_login import current_user, fresh_login_required, LoginManager, login_required, login_user, logout_user
import ipaddress
import secrets
import socket

# Create/configure the app
app = Flask('isharmud')
app.config.from_pyfile('config.py')

# Static root paths
@app.route('/favicon.ico')
@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message_category            = 'error'
login_manager.login_view                        = 'login'
login_manager.needs_refresh_message             = 'To protect your account, please log in again.'
login_manager.needs_refresh_message_category    = 'error'
login_manager.refresh_view                      = 'login'
login_manager.session_protection                = 'strong'

# Get database and form classes
import models
import forms

# Get users for the Flask Login Manager via Account object from the database
@login_manager.user_loader
def load_user(account_id):
    return models.Account.query.get(str(account_id))

# Add context processors
@app.context_processor
def injects():
    return dict(
            now             = datetime.datetime.now().timestamp(),
            season          = models.Season.query.filter_by(is_active = 1).first(),
            immortal_level  = secrets.immortal_level
    )

# Handle errors with a little template
def error(title='Unknown Error', message='Sorry, but there was an unknown error.', code=500):
    return render_template('error.html.j2', title=title, message=message), code

@app.errorhandler(400)
def bad_request(message):
    return error(title='Bad Request', message=message, code=400)

@app.errorhandler(401)
def not_authorized(message):
    return error(title='Not Authorized', message=message, code=401)

@app.errorhandler(403)
def forbidden(message):
    return error(title='Forbidden', message=message, code=403)

@app.errorhandler(404)
def page_not_found(message):
    return error(title='Page Not Found', message=message, code=404)

@app.errorhandler(500)
def internal_server_error(message):
    return error(title='Internal Server Error', message=message, code=500)


# Main welcome page/index (/)
@app.route('/welcome', methods=['GET'])
@app.route('/', methods=['GET'])
def welcome():
    # Find the two (2) most recent news posts to show on the main page
    news = models.News.query.order_by(-models.News.created_at).limit(1).all()
    return render_template('welcome.html.j2', news=news)


# /history (or /background)
@app.route('/background', methods=['GET'])
@app.route('/history', methods=['GET'])
def history():
    return render_template('history.html.j2')


# Log in (/login)
@app.route('/login', methods=['GET', 'POST'])
def login():

    # Get log in form object and check if submitted
    login_form = forms.LoginForm()
    if login_form.validate_on_submit():

        # Find the user by e-mail address from the log in form
        account = models.Account.query.filter_by(email = login_form.email.data).first()

        # If we find the user email and match the password, it is a successful log in
        if account != None and account.check_password(login_form.password.data):
            flash('You have logged in!', 'success')
            login_user(account, remember=login_form.remember.data)

        # There must have been invalid credentials
        else:
            flash('Sorry, but please enter a valid e-mail address and password.', 'error')

    # Redirect users who are logged in to the portal
    if current_user.is_authenticated:
        try:
            return redirect(session['next'])
        except:
            return redirect(url_for('portal'))

    # Show the log in form
    return render_template('login.html.j2', login_form=login_form), 401


# Allow logged in users to change their passwords
@app.route('/password', methods=['GET', 'POST'])
@fresh_login_required
def change_password():

    # Get change password form object and check if submitted
    change_password_form = forms.ChangePasswordForm()
    if change_password_form.validate_on_submit():

        # Proceed if the user is authenticated and entered their current password correctly
        if current_user.is_authenticated and current_user.check_password(change_password_form.current_password.data):
            if current_user.change_password(change_password_form.confirm_new_password.data):
                flash('Your password has been changed!', 'success')
            else:
                flash('Sorry, but your password could not be changed.', 'error')

        # Otherwise, tell them to enter their current password correctly
        else:
            flash('Please enter your current password correctly!', 'error')

    # Show the change password form
    return render_template('change_password.html.j2', change_password_form=change_password_form)


# Process player search
@app.route('/player/search', methods=['POST'])
@login_required
def search_player(player_name=None):
    player_search_form = forms.PlayerSearchForm()
    if player_search_form.validate_on_submit():
        player_search = models.Player.query.filter(models.Player.name.like(player_search_form.player_search_name.data + '%')).first()
    try:
        player_name = player_search.name
    except Exception as e:
        player_name = None
        print(e)
    return redirect(url_for('show_player', player_name=player_name))


# Player pages
@app.route('/player', methods=['GET'])
@app.route('/player/<string:player_name>', methods=['GET'])
@login_required
def show_player(player_name=None):

    try:
        find_player = models.Player.query.filter_by(name = player_name).first()
        code = 200
    except Exception as e:
        print(e)
        find_player = None
        flash('Sorry, but please choose a valid player!', 'error')
        code = 404

    return render_template('player.html.j2',
                                player              = find_player,
                                player_search_form  = forms.PlayerSearchForm()
                            ), code


# Portal for logged in users
@app.route('/portal', methods=['GET'])
@login_required
def portal():
    # Show the portal
    return render_template('portal.html.j2',
                                is_admin    = current_user.is_admin(secrets.admin_level)
                            )


# Challenges page for logged in users
@app.route('/challenges', methods=['GET'])
def challenges():
    # Show the current challenges
    return render_template('challenges.html.j2',
                                challenges  = models.Challenge.query.filter_by(is_active = 1).order_by(
                                                    models.Challenge.winner_desc,
                                                    -models.Challenge.adj_tier
                                                ).all()
                          )


# Sort and list the best players for Leader Board page for logged in users
@app.route('/leader_board/<int:limit>', methods=['GET'])
@app.route('/leaderboard/<int:limit>', methods=['GET'])
@app.route('/leader_board', methods=['GET'])
@app.route('/leaderboard', methods=['GET'])
def leaderboard(limit=10):
    if limit > max([5, 10, 25, 50, 100]):
        return redirect(url_for('leaderboard', limit=10))

    return render_template('leaderboard.html.j2',
                                leaders         =   models.Player.query.filter(
                                                        models.Player.true_level < secrets.immortal_level
                                                    ).order_by(
                                                        -models.Player.remorts,
                                                        -models.Player.total_renown,
                                                        -models.Player.quests_completed,
                                                        -models.Player.challenges_completed,
                                                        -models.Player.renown,
                                                        -models.Player.level,
                                                        -models.Player.bankacc,
                                                        models.Player.deaths
                                                    ).limit(limit).all(),
                                limit           =   limit
                          )


# Show online users (who)
@app.route('/who', methods=['GET'])
@login_required
def who():
    return render_template('who.html.j2',
                                who =   models.Player.query.filter(
                                            models.Player.true_level < secrets.immortal_level,
                                            models.Player.logon == models.Player.logout
                                        ).order_by(
                                            -models.Player.level,
                                            -models.Player.remorts,
                                            -models.Player.total_renown,
                                            -models.Player.quests_completed,
                                            -models.Player.challenges_completed,
                                            -models.Player.renown,
                                            -models.Player.bankacc,
                                            models.Player.deaths
                                        ).all()
                            )


# Portal for administrators
@app.route('/admin', methods=['GET', 'POST'])
@fresh_login_required
def admin_portal():

    # Redirect non-administrators to the main page
    if not current_user.is_admin(secrets.admin_level):
        flash('Sorry, but you are not an administrator!', 'error')
        return redirect(url_for('welcome'))

    # Get news add form and check if submitted
    news_add_form = forms.NewsAddForm()
    if news_add_form.validate_on_submit():

        # Create the model for the new news post
        new_news = models.News(
            account_id      = current_user.account_id,
            created_at      = datetime.datetime.now(),
            subject         = news_add_form.subject.data,
            body            = news_add_form.body.data
        )

        # Create the news post in the database, get the news post ID, and check that it worked
        created_id = new_news.add_news()
        created_post = models.News.query.filter_by(news_id = created_id).first()
        if created_post:
            flash('Your message has been posted!', 'success')
        else:
            flash('Sorry, but please try again!', 'error')

    # Show the form to add news in the administration portal
    return render_template('admin.html.j2', news_add_form=news_add_form)


# /logout
@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('You have logged out!', 'success')
    return welcome()


# Allow anonymous users to create a new account
@app.route('/new', methods=['GET', 'POST'])
def new_account():

    # Get new account form object and check if submitted
    new_account_form = forms.NewAccountForm()
    if new_account_form.validate_on_submit():

        # Check that e-mail address has not already been used
        find_email = models.Account.query.filter_by(email = new_account_form.email.data).first()
        if find_email:
            flash('Sorry, but that e-mail address exists. Please log in.', 'error')
            return redirect(url_for('login'))

        # Check that the account name is not in use
        find_name = models.Account.query.filter_by(account_name = new_account_form.account_name.data).first()
        if find_name:
            flash('Sorry, but that account name is already being used!', 'error')

        # Otherwise, proceed in trying to create the new account
        else:
            ip_address  = ipaddress.ip_address(request.remote_addr)
            new_account = models.Account(
                email           = new_account_form.email.data,
                password        = new_account_form.confirm_password.data,
                create_isp      = ip_address,
                last_isp        = '',
                create_ident    = '',
                last_ident      = '',
                create_haddr    = int(ip_address),
                last_haddr      = int(ip_address),
                account_name    = new_account_form.account_name.data
            )

            # Create the account in the database, get the account ID, and log the user in
            created_id      = new_account.create_account()
            created_account = models.Account.query.filter_by(account_id = created_id).first()
            if created_account:
                login_user(created_account)
                flash('Your account has been created!', 'success')
            else:
                flash('Sorry, but please try again!', 'error')

    # Redirect users who are logged in to the portal, including newly created accounts
    if current_user.is_authenticated:
        return redirect(url_for('portal'))

    # Show the new account form
    return render_template('new.html.j2', new_account_form=new_account_form)

# /clients or /mud_clients
@app.route('/clients', methods=['GET'])
@app.route('/mud_clients', methods=['GET'])
def mud_clients():
    import mud_clients
    return render_template('mud_clients.html.j2', mud_clients=mud_clients.mud_clients)


# Redirect /connect to mudslinger.net
@app.route('/connect', methods=['GET'])
def connect():
    mudslinger_app_link = 'https://mudslinger.net/play/?host=isharmud.com&port=23'
    return redirect(mudslinger_app_link)


# Redirect /discord to the invite link
@app.route('/discord', methods=['GET'])
def discord():
    discord_invite_link = 'https://discord.gg/VBmMXUpeve'
    return redirect(discord_invite_link)


@app.route('/latest_patch', methods=['GET'])
def latest_patch(patch_directory='static/patches/'):
    import glob
    import os
    pdfs    = glob.glob(patch_directory + '*.pdf')
    latest  = max(pdfs, key=os.path.getctime)
    return redirect(latest)


# /faq (or /faqs or /questions)
@app.route('/questions')
@app.route('/faqs')
@app.route('/faq')
def faq():
    import faq
    return render_template('faq.html.j2', faqs=faq.faqs)


# /get_started
@app.route('/gettingstarted')
@app.route('/getting_started')
@app.route('/getstarted')
@app.route('/get_started')
def get_started():
    return render_template('get_started.html.j2')


# /support (or /donate)
@app.route('/donate', methods=['GET'])
@app.route('/support', methods=['GET'])
def support():
    return render_template('support.html.j2')


# /world (or /areas)
@app.route('/areas/<string:area>', methods=['GET'])
@app.route('/areas', methods=['GET'])
@app.route('/world/<string:area>', methods=['GET'])
@app.route('/world', methods=['GET'])
def world(area=None):

    # Try to find an area based on user input
    try:
        areas   = helptab._get_help_area(helptab_file=secrets.helptab_file, area=area)
        code    = 200

    # Otherwise, list all areas found in the game "helptab" file
    except Exception as e:
        print(e)
        flash('Sorry, but please choose a valid area!', 'error')
        areas   = helptab._get_help_area(None)
        area    = None
        code    = 404

    return render_template('world.html.j2', areas=areas, area=area), code


# Jinja2 template filter to convert UNIX timestamps to Python date-time objects
@app.template_filter('unix2datetime')
def unix2datetime(unix_time):
    return datetime.datetime.fromtimestamp(unix_time)


# Jinja2 template filter to convert seconds to human-readable delta
@app.template_filter('seconds2delta')
def seconds2delta(seconds):
    return datetime.timedelta(seconds=seconds)


import helptab
