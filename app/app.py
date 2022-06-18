import secrets
import datetime
from flask import abort, Flask, flash, redirect, render_template, url_for
from flask_login import current_user, LoginManager, login_required, login_user, logout_user

# Create/configure the app
app = Flask('ishar')
app.config.from_pyfile('config.py')

# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message_category    = 'error'
login_manager.login_view                = 'login'
login_manager.session_protection        = 'strong'

import models

# Get users for the Flask Login Manager via Account object from the database
@login_manager.user_loader
def load_user(account_id):
    return models.Account.query.get(int(account_id))

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
        user = models.Account.query.filter_by(email = login_form.email.data).first()

        # If we find the user email and match the password, it is a successful log in, so redirect to portal
        if user != None and user.check_password(login_form.password.data):
            flash('You have logged in!', 'success')
            print(login_form.remember.data)
            login_user(user, remember=login_form.remember.data)
            return redirect(url_for('portal'), code=302)

        # There must have been invalid credentials
        else:
            flash('Sorry, but please enter a valid e-mail address and password.', 'error')

    # Make sure the user is logged out and show the log in form
    logout_user()
    return render_template('login.html.j2', login_form=login_form)


# Portal for logged in users
@app.route('/portal', methods=['GET'])
@login_required
def portal():

    # Find the current season information and show the portal
    season = models.Season.query.filter_by(is_active = 1).first()
    return render_template('portal.html.j2', season=season)


# /logout
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have logged out!', 'success')
    return login()


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
    return datetime.datetime.fromtimestamp(unix_time).strftime('%c')


import helptab
