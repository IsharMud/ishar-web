import secrets
import crypt
import datetime
from flask import abort, Flask, flash, make_response, redirect, render_template, request, url_for
from flask_login import current_user, LoginManager, login_required, login_user, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
import hmac
from sqlalchemy import Column, DateTime, ForeignKey, Integer, MetaData, SmallInteger, String, Table
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship

# Create/configure the app
app = Flask('ishar')
app.config.from_pyfile('config.py')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)

# Account database class
class Account(db.Model, UserMixin):
    __tablename__ = 'accounts'
    account_id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    seasonal_points = Column(Integer, nullable=False, server_default=FetchedValue())
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(36), nullable=False)
    create_isp = Column(String(25), nullable=False)
    last_isp = Column(String(25), nullable=False)
    create_ident = Column(String(25), nullable=False)
    last_ident = Column(String(25), nullable=False)
    create_haddr = Column(Integer, nullable=False)
    last_haddr = Column(Integer, nullable=False)
    account_name = Column(String(25), nullable=False, unique=True)
    players = relationship('Player', lazy='select', backref='account')

    def check_password(self, password):
        return hmac.compare_digest(crypt.crypt(password, self.password), self.password)

    def get_id(self):
        return str(self.account_id)

    def is_authenticated(self):
        return isinstance(self.account_id, int)

    def is_active(self):
        return isinstance(self.account_id, int)

    def check_password(self, password):
        return hmac.compare_digest(crypt.crypt(password, self.password), self.password)


# Player database class
class Player(db.Model):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    account_id = Column(ForeignKey('accounts.account_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    name = Column(String(15), nullable=False, unique=True, server_default=FetchedValue())
    create_ident = Column(String(10), nullable=False, server_default=FetchedValue())
    last_isp = Column(String(30), nullable=False, server_default=FetchedValue())
    description = Column(String(240))
    title = Column(String(45), nullable=False, server_default=FetchedValue())
    poofin = Column(String(80), nullable=False, server_default=FetchedValue())
    poofout = Column(String(80), nullable=False, server_default=FetchedValue())
    bankacc = Column(Integer, nullable=False)
    logon_delay = Column(SmallInteger, nullable=False)
    true_level = Column(Integer, nullable=False)
    renown = Column(Integer, nullable=False)
    prompt = Column(String(42), nullable=False, server_default=FetchedValue())
    remorts = Column(Integer, nullable=False)
    favors = Column(Integer, nullable=False)
    birth = Column(Integer, nullable=False)
    logon = Column(Integer, nullable=False)
    online = Column(Integer)
    logout = Column(Integer, nullable=False)
    bound_room = Column(Integer, nullable=False)
    load_room = Column(Integer, nullable=False)
    wimpy = Column(SmallInteger)
    invstart_level = Column(Integer)
    color_scheme = Column(SmallInteger)
    sex = Column(Integer, nullable=False)
    race_id = Column(ForeignKey('races.race_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    class_id = Column(ForeignKey('classes.class_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    level = Column(Integer, nullable=False)
    weight = Column(SmallInteger, nullable=False)
    height = Column(SmallInteger, nullable=False)
    align = Column(SmallInteger, nullable=False)
    comm = Column(SmallInteger, nullable=False)
    karma = Column(SmallInteger, nullable=False)
    experience_points = Column(Integer, nullable=False)
    money = Column(Integer, nullable=False)
    fg_color = Column(SmallInteger, nullable=False)
    bg_color = Column(SmallInteger, nullable=False)
    login_failures = Column(SmallInteger, nullable=False)
    create_haddr = Column(Integer, nullable=False)
    auto_level = Column(Integer, nullable=False)
    login_fail_haddr = Column(Integer)
    last_haddr = Column(Integer)
    last_ident = Column(String(10), server_default=FetchedValue())
    load_room_next = Column(Integer)
    load_room_next_expires = Column(Integer)
    aggro_until = Column(Integer)
    inn_limit = Column(SmallInteger, nullable=False)
    held_xp = Column(Integer)
    last_isp_change = Column(Integer)
    perm_hit_pts = Column(Integer, nullable=False)
    perm_move_pts = Column(Integer, nullable=False)
    perm_spell_pts = Column(Integer, nullable=False)
    perm_favor_pts = Column(Integer, nullable=False)
    curr_hit_pts = Column(Integer, nullable=False)
    curr_move_pts = Column(Integer, nullable=False)
    curr_spell_pts = Column(Integer, nullable=False)
    curr_favor_pts = Column(Integer, nullable=False)
    init_strength = Column(Integer, nullable=False)
    init_agility = Column(Integer, nullable=False)
    init_endurance = Column(Integer, nullable=False)
    init_perception = Column(Integer, nullable=False)
    init_focus = Column(Integer, nullable=False)
    init_willpower = Column(Integer, nullable=False)
    curr_strength = Column(Integer, nullable=False)
    curr_agility = Column(Integer, nullable=False)
    curr_endurance = Column(Integer, nullable=False)
    curr_perception = Column(Integer, nullable=False)
    curr_focus = Column(Integer, nullable=False)
    curr_willpower = Column(Integer, nullable=False)
    is_deleted = Column(Integer, nullable=False, server_default=FetchedValue())
    deaths = Column(Integer, nullable=False, server_default=FetchedValue())
    total_renown = Column(Integer, nullable=False, server_default=FetchedValue())
    quests_completed = Column(Integer, nullable=False, server_default=FetchedValue())
    challenges_completed = Column(Integer, nullable=False, server_default=FetchedValue())


# Login Manager user loader from database
@login_manager.user_loader
def load_user(account_id):
    return Account.query.get(int(account_id))

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

# /background
@app.route('/background')
def background():
    return render_template('background.html.j2')

# Log-in form or processing (/login)
@app.route('/login', methods=['GET', 'POST'])
def login():

    # If someone is trying to log in (submitted the form), process it
    if request.method == 'POST':

        # Try to find the user account by e-mail address
        user = Account.query.filter_by(email = request.form['email']).first()

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
        return render_template('portal.html.j2')
    except Exception as e:
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

# /help
@app.route('/help', methods=['GET'])
@app.route('/help/<string:page>', methods=['GET'])
def help(page=None):
    return render_template('help.html.j2', page=page)

# /clients
@app.route('/clients')
def clients():

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

    return render_template('clients.html.j2', mud_clients=mud_clients)


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

# /getstarted
@app.route('/gettingstarted')
@app.route('/getting_started')
@app.route('/get_started')
@app.route('/getstarted')
def getting_started():
    return render_template('getting_started.html.j2')

# /areas (formerly "world" page)
@app.route('/areas', methods=['GET'])
@app.route('/areas/<string:area>', methods=['GET'])
def areas(area=None):

    # Try to find an area based on user input
    try:
        areas = _get_help_area(area)
        code = 200

    # Otherwise, list all areas found in the game "helptab" file
    except Exception as e:
        areas = _get_help_area(None)
        area = None
        code = 404
        print(f"Bad area? {e}")

    return render_template('areas.html.j2', areas=areas, area=area), code


# Internal function to scrape "areas" from game helptab file
#
# The "areas" are each listed in the "helptab" file on lines starting with "32 Area " ...
# ...followed by descriptions until the character "#" on a single line itself
def _get_help_area(area=None):

    # Get game "helptab" file path/name, and open it
    helptab_file = secrets.helptab_file
    helptab_fh = open(helptab_file, 'r')

    # Prepare an empty "areas" dictionary
    areas = {}

    # Do not keep lines by default
    keep = False

    # Loop through each line, finding and keeping chunks staring with "32 Area "
    for line in helptab_fh:
        stripped = line.strip()

        # Stop line (#)
        if keep == True and stripped == '#':
            keep = False

        # Do not include "other levels" info (%%)
        if keep == True and stripped.startswith('%% '):
            keep = False

        # Append the current chunk to our areas dictionary, under the key of whatever started with "32 Area " last
        if keep == True and not stripped.startswith('32 Area '):
            areas[area_name] += line

        # Start new dictionary keys of chunks at lines beginning with "32 Area "
        if stripped.startswith('32 Area '):
            keep = True
            area_name = stripped.replace('32 Area ', '')
            areas[area_name] = ''

    # Close the "helptab" file
    helptab_fh.close()

    # Return either the single area, or a list of them
    if area != None and areas[area]:
        return areas[area]
    elif areas != None and len(areas) > 0:
        return areas
    else:
        return None


# Jinja2 template filter to convert UNIX timestamps to Python date-time objects
@app.template_filter('unix2human_time')
def unix2human_time(unix_time):
    return datetime.datetime.fromtimestamp(unix_time).strftime('%c')
