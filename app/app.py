import secrets
import datetime
from flask import abort, Flask, flash, make_response, redirect, render_template, request, url_for
from flask_login import current_user, LoginManager, login_required, login_user, logout_user

# Create/configure the app
app = Flask('ishar')
app.config.from_pyfile('config.py')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

import models

# Login Manager user loader from database
@login_manager.user_loader
def load_user(account_id):
    return models.Account.query.get(int(account_id))

# Errors
def error(title='Unknown Error', message='Sorry, but we experienced an unknown error', code=500):
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
@app.route('/welcome')
@app.route('/')
def welcome():
    return render_template('welcome.html.j2')

# /history (formerly "Background" page)
@app.route('/history')
def history():
    return render_template('history.html.j2')

# Log-in form or processing (/login)
@app.route('/login', methods=['GET', 'POST'])
def login():

    # If someone is trying to log in (submitted the form), process it
    if request.method == 'POST':

        # Try to find the user account by e-mail address
        user = models.Account.query.filter_by(email = request.form['email']).first()

        # If we find the user and match the password, it is a successful log in, so redirect
        if user != None and user.check_password(request.form['password']):
            flash('You successfully logged in!', 'success')
            login_user(user)
            return redirect(url_for('portal'), code=302)

        # Otherwise, there must have been invalid credentials
        else:
            flash('Sorry, but please enter a valid e-mail address and password.', 'error')

    # # Redirect authenticated users to the portal
    if current_user.is_authenticated:
        return redirect(url_for('portal'), code=302)
    else:
        # Log-in form
        return render_template('login.html.j2')


# Portal for logged in users
@app.route('/portal', methods=['GET'])
@login_required
def portal():
    try:
        print(f"Portal visit: {current_user}")
        season = models.Season.query.filter_by(is_active = 1).first()
        return render_template('portal.html.j2', season=season)
    except Exception as e:
        logout_user()
        print(f"Portal exception: {e}")
        flash('Sorry, but there was an error visiting the portal!', 'error')
        return login()

# /logout (log out)
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    try:
        logout_user()
        flash('You have been logged out successfully! See you again next time!', 'success')
        return login()
    except Exception as e:
        print(f"Logout exception: {e}")
        flash('Sorry, but there was an error logging you out!', 'error')
        return login()


# /clients or /mud_clients
@app.route('/clients')
@app.route('/mud_clients')
def mud_clients():

    mud_clients = {
        "Cross-Platform" : {
            'Mudlet' : 'https://www.mudlet.org/'
        },
        "Android" : {
            'Blowtorch' : 'http://bt.happygoatstudios.com/'
        },
        "Windows" : {
            'ZMud' : 'http://www.zuggsoft.com/zmud/zmudinfo.htm',
            'alclient' : 'http://www.ashavar.com/client/',
            'yTin' : 'http://ytin.sourceforge.net/',
            'Gosclient' : 'http://gosclient.altervista.org/eng/',
            'MUSHclient' : 'http://www.gammon.com.au/downloads/dlmushclient.htm'
        },
        "Mac OS" : {
            'Atlantis' : 'http://www.riverdark.net/atlantis/',
            'MudWalker' : 'http://mudwalker.cubik.org/'
        },
        "Linux / UNIX" : {
            'TinTin++' : 'http://tintin.sourceforge.net/',
            'TinyFugue' : 'http://tinyfugue.sourceforge.net/'
        }
    }

    return render_template('mud_clients.html.j2', mud_clients=mud_clients)


# Redirect /connect to mudslinger.net
@app.route('/connect')
def connect():
    mudslinger_app_link = 'https://mudslinger.net/play/?host=isharmud.com&port=23'
    return redirect(mudslinger_app_link, code=302)

# Redirect /discord to the invite link
@app.route('/discord')
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

# /support
@app.route('/donate')
@app.route('/support')
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
        areas = helptab._get_help_area(area)
        code = 200

    # Otherwise, list all areas found in the game "helptab" file
    except Exception as e:
        areas = helptab._get_help_area(None)
        area = None
        code = 404
        print(f"Bad area? {e}")

    return render_template('world.html.j2', areas=areas, area=area), code


# Jinja2 template filter to convert UNIX timestamps to Python date-time objects
@app.template_filter('unix2human_time')
def unix2human_time(unix_time):
    return datetime.datetime.fromtimestamp(unix_time).strftime('%c')

import helptab
