import secrets
import crypt
from flask import abort, Flask, flash, make_response, redirect, render_template, request, url_for
from flask_login import current_user, LoginManager, login_required, login_user, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
import hmac
from sqlalchemy import Column, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT

# Create/configure the app
app = Flask('ishar')
app.config.from_pyfile('config.py')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)

# Account database class
class account(db.Model, UserMixin):
    __tablename__ = 'accounts'
    account_id = Column(INTEGER(11), primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))
    seasonal_points = Column(TINYINT(4), nullable=False, server_default=text("0"))
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(36), nullable=False)
    create_isp = Column(String(25), nullable=False)
    last_isp = Column(String(25), nullable=False)
    create_ident = Column(String(25), nullable=False)
    last_ident = Column(String(25), nullable=False)
    create_haddr = Column(INTEGER(11), nullable=False)
    last_haddr = Column(INTEGER(11), nullable=False)
    account_name = Column(String(25), nullable=False, unique=True)

    def get_id(self):
        return str(self.account_id)

    def check_password(self, password):
        return hmac.compare_digest(crypt.crypt(password, self.password), self.password)


# Login Manager user loader from database
@login_manager.user_loader
def load_user(account_id):
    return account.query.get(int(account_id))

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

    if current_user.is_authenticated:
        return redirect('/portal')

    if request.method == 'POST':
        email = request.form['email']
        user = account.query.filter_by(email = email).first()
        print(user)

        if user != None and user.check_password(request.form['password']):
            flash('You successfully logged in!')
            login_user(user)
        else:
            flash('Sorry, but please enter a valid e-mail address and password.')

    return render_template('login.html.j2')

# /logout (log out)
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    try:
        logout_user()
        flash('You have been logged out!')
        return login()
    except:
        return error()

# /portal (log in required)
@app.route('/portal', methods=['GET'])
@login_required
def portal(user=current_user):
    return render_template('portal.html.j2', user=user)

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
