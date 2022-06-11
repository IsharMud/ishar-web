import secrets
from flask import Flask, flash, make_response, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, TINYINT

# Create/configure the app
app = Flask('ishar')
login_manager = LoginManager()
app.config.from_pyfile('config.py')
login_manager.init_app(app)
db = SQLAlchemy(app)

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

@login_manager.user_loader
def load_user(account_id):
    return account.get(account_id)

# Errors (404)
@app.errorhandler(404)
def page_not_found(message):
    return render_template('error.html.j2', title='Page Not Found', message=message), 404

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
    if request.method == 'POST':
        if request.form['email'] != 'admin@isharmud.com' or request.form['password'] != 'secret':
            flash('Please enter your e-mail address and password to log in.')
        else:
            flash('You were successfully logged in!')

    return render_template('login.html.j2')

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
        if keep and stripped.startswith('%% '):
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
