import datetime
from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user, fresh_login_required, LoginManager, login_required, login_user, logout_user
import ipaddress
import secrets
import socket

# Create/configure the app
app = Flask('ishar')
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

import models

# Get users for the Flask Login Manager via Account object from the database
@login_manager.user_loader
def load_user(account_id):
    return models.Account.query.get(str(account_id))

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
    return render_template('welcome.html.j2')


# /history (or /background)
@app.route('/background', methods=['GET'])
@app.route('/history', methods=['GET'])
def history():
    return render_template('history.html.j2')


# Log in (/login)
@app.route('/login', methods=['GET', 'POST'])
def login():

    # Get log in form object and check if submitted
    login_form = models.LoginForm()
    if login_form.validate_on_submit():

        # Find the user by e-mail address from the log in form
        account = models.Account.query.filter_by(email = login_form.email.data).first()

        # If we find the user email and match the password, it is a successful log in, so redirect to portal
        if account != None and account.check_password(login_form.password.data):
            flash('You have logged in!', 'success')
            login_user(account, remember=login_form.remember.data)
            return redirect(url_for('portal'), code=302)

        # There must have been invalid credentials
        else:
            flash('Sorry, but please enter a valid e-mail address and password.', 'error')

    # Make sure the user is logged out and show the log in form
    logout_user()
    return render_template('login.html.j2', login_form=login_form)


# Allow logged in users to change their passwords
@app.route('/password', methods=['GET', 'POST'])
@fresh_login_required
def change_password():

    # Get change password form object and check if submitted
    change_password_form = models.ChangePasswordForm()
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


# Portal for logged in users
@app.route('/portal', methods=['GET'])
@login_required
def portal():

    # Find the current season information and show the portal
    season = models.Season.query.filter_by(is_active = 1).first()
    return render_template('portal.html.j2', season=season, is_admin=current_user.is_admin())


# /logout
@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('You have logged out!', 'success')
    return login()


# Allow anonymous users to create a new account
@app.route('/new', methods=['GET', 'POST'])
def new_account():

    # Get new account form object and check if submitted
    new_account_form = models.NewAccountForm()
    if new_account_form.validate_on_submit():

        # Check that e-mail address has not already been used
        find_email = models.Account.query.filter_by(email = new_account_form.email.data).first()
        if find_email:
            flash('Sorry, but that e-mail address exists. Please log in.', 'error')
            return redirect(url_for('login'), code=302)

        # Check that the account name is not in use
        find_name = models.Account.query.filter_by(account_name = new_account_form.account_name.data).first()
        if find_name:
            flash('Sorry, but that account name is already being used!', 'error')

        # Otherwise, proceed in trying to create the new account
        else:
            ip_address = ipaddress.ip_address(request.remote_addr)
            new_account = models.Account(
                email           = new_account_form.email.data,
                password        = new_account_form.confirm_password.data,
                ##########
                # FIX ME #
                ##########
                create_isp      = '',
                last_isp        = '',
                create_ident    = '',
                last_ident      = '',
                ##########
                # FIX ME #
                ##########
                create_haddr    = int(ip_address),
                last_haddr      = int(ip_address),
                account_name    = new_account_form.account_name.data
            )

            # Create the account in the database, get the account ID, and log the user in
            created_id = new_account.create_account()
            created_account = models.Account.query.filter_by(account_id = created_id).first()
            if created_account:
                login_user(created_account)
                flash('Your account has been created!', 'success')
            else:
                flash('Sorry, but please try again!', 'error')

    # Redirect users who are logged in to the portal, including newly created accounts
    if current_user.is_authenticated:
        return redirect(url_for('portal'), code=302)

    # Show the new account form
    return render_template('new.html.j2', new_account_form=new_account_form)

# /clients or /mud_clients
@app.route('/clients', methods=['GET'])
@app.route('/mud_clients', methods=['GET'])
def mud_clients():

    mud_clients = {
        'Cross-Platform' : {
            'Mudlet'        : 'https://www.mudlet.org/'
        },
        'Android' : {
            'Blowtorch' : 'http://bt.happygoatstudios.com/'
        },
        'Windows' : {
            'ZMud'          : 'https://www.zuggsoft.com/zmud/zmudinfo.htm',
            'alclient'      : 'https://www.ashavar.com/client/',
            'yTin'          : 'http://ytin.sourceforge.net/',
            'Gosclient'     : 'http://gosclient.altervista.org/eng/',
            'MUSHclient'    : 'https://www.gammon.com.au/downloads/dlmushclient.htm',
        },
        'Mac OS' : {
            'Atlantis'      : 'https://www.riverdark.net/atlantis/',
            'MudWalker'     : 'http://mudwalker.cubik.org/'
        },
        'Linux / UNIX' : {
            'TinTin++'      : 'http://tintin.sourceforge.net/',
            'TinyFugue'     : 'http://tinyfugue.sourceforge.net/'
        }
    }

    return render_template('mud_clients.html.j2', mud_clients=mud_clients)


# Redirect /connect to mudslinger.net
@app.route('/connect', methods=['GET'])
def connect():
    mudslinger_app_link = 'https://mudslinger.net/play/?host=isharmud.com&port=23'
    return redirect(mudslinger_app_link, code=302)


# Redirect /discord to the invite link
@app.route('/discord', methods=['GET'])
def discord():
    discord_invite_link = 'https://discord.gg/VBmMXUpeve'
    return redirect(discord_invite_link, code=302)

# /faq (or /faqs or /questions)
@app.route('/questions')
@app.route('/faqs')
@app.route('/faq')
def faq():

    faqs = {

            'Is Ishar MUD free?': [
                "<strong>Yes!</strong> While you are more than welcome to " \
                " <a href=\"" + url_for('support') + "\">offer support</a>, " \
                "Ishar MUD is free to use, play, and enjoy."
            ],

            'Are there player classes?': [
                '<strong>Yes!</strong> There are five (5) player classes:',
                ['Cleric', 'Magician', 'Necromancer', 'Rogue', 'Warrior']
            ],

            'Is there role-playing?': [
                '<strong>No.</strong> Ishar MUD does not require role-playing.'
            ],

            'What about my equipment when I log out?': [
                'When you sign out or log off, your character\'s equipment, gear, ' \
                'and inventory is simply <strong>preserved until the end of the season</strong>.',
                'The season currently changes every four (4) months.'
            ],

            'Is death permanent?': [
                'When first creating a character, <strong>you can choose</strong> whether to play in "Survival" (aka "perma-death") or "Classic" mode.',
                "While survival mode gains experience faster, classic mode subtracts experience upon death, but allows you to retrieve your character's corpse."
            ],

            'Can I have multiple characters or multi-play?': [
                'You may only have a single account with up to <strong>ten (10) characters per account</strong>.',
                'You may actively <strong>multi-play up to three (3) characters at once</strong>.'
            ],

            'Is there player-killing (PK) or player-versus-player (PvP) combat?': [
                '<strong>Yes and no...</strong>',
                "While player-versus-player combat (or PK'ing) is possible, it is very rare and not a requirement of the game."
            ]
    }

    return render_template('faq.html.j2', faqs=faqs)


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
def world(area=None, code=200):

    # Try to find an area based on user input
    try:
        areas = helptab._get_help_area(area)

    # Otherwise, list all areas found in the game "helptab" file
    except Exception as e:
        flash('Sorry, but please choose a valid area!', 'error')
        areas = helptab._get_help_area(None)
        area = None
        code = 404

    return render_template('world.html.j2', areas=areas, area=area), code


# Jinja2 template filter to convert UNIX timestamps to Python date-time objects
@app.template_filter('unix2human_time')
def unix2human_time(unix_time):
    return datetime.datetime.fromtimestamp(unix_time).strftime('%A, %B %d, %Y %I:%M %p %Z')


import helptab
