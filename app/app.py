import secrets
from flask import Flask, flash, make_response, redirect, render_template, request, url_for

# Create the "app" (as uwsgi expects)
app = Flask(__name__)
app.config.from_pyfile('config.py')


# Errors (404)
@app.errorhandler(404)
def page_not_found(message):
    return render_template('error.html.j2', title='Page Not Found', message=message), 404

# Main index page (/)
@app.route('/')
def index():
    return render_template('index.html.j2')

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
@app.route('/help/<string:letter>')
@app.route('/help/<string:letter>/')
@app.route('/help/<string:letter>/<string:page>.html')
def help(letter=None, page=None):
    return render_template('help.html.j2', letter=letter, page=page)

# Search help (POST /help) / WIP!!!
@app.route('/help', methods=['POST'])
def search_help(search_help=None):
    if request.form['search_help'] and request.form['search_help'] != '':
        search_help = request.form['search_help']
        return help(letter=search_help[0], page=search_help)
    else:
        return help()

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
    return redirect('https://mudslinger.net/play/?host=isharmud.com&port=23', code=302)

# Redirect /discord to the invite link (in config.py)
@app.route('/discord')
def discord():
    discord_invite_link = 'https://discord.gg/VBmMXUpeve'
    return redirect(config.discord_invite_link, code=302)

# /world
@app.route('/world')
def world():
    return render_template('world.html.j2')
