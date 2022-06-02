import config
import secrets
from flask import Flask, redirect, render_template, request, url_for
import mariadb

# Name the "app" (as uwsgi expects)
app = Flask(__name__)

# Internal function to connect to the database
def _db_connect(user=secrets.db_creds['user'], password=secrets.db_creds['password'], host=secrets.db_creds['host'], port=secrets.db_creds['port'], database=secrets.db_creds['database']):

    try:
        conn = mariadb.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )

        return conn

    except mariadb.Error as e:
        print(e)
        return False
    except Exception as e:
        print(e)
        return e


# Internal function to validate e-mail address and password from the log in form
def _check_credentials(email, password):

    if not email or email == '':
        return False

    if not password or password == '':
        return False

    try:
        dbc = _db_connect()
        cur = dbc.cursor()
        dbc.close()
    except Exception as e:
        print(e)

# /clients
@app.route('/clients')
def clients(mud_clients=config.mud_clients):
    return render_template('clients.html.j2', mud_clients=mud_clients)

# Redirect /connect to mudslinger.net
@app.route('/connect')
def connect():
    return redirect('https://mudslinger.net/play/?host=isharmud.com&port=23', code=302)

# Redirect /discord to the link listed in secrets.py
@app.route('/discord')
def discord():
    return redirect(config.discord_invite_link, code=302)

def error(title='Page Not Found', message='Hmmm... the page you are looking for can not be found.', code=404):
    return render_template('error.html.j2', title=title, message=message), code

# /help in progress
@app.route('/help')
@app.route('/help/<string:page>')
def help(page=None):
    return render_template('help.html.j2', page=page)

@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html.j2')

# POST /login, Process Log In attempt and welcome user
@app.route('/login', methods=['POST'])
def process_login():

    try:
        email =  request.form['email']
        password =  request.form['password']

        if not email or email == '':
            return error(title='Invalid E-mail Address', message='Sorry, but please enter a valid e-mail address.', code=400)

        if not password or password == '':
            return error(title='Invalid Password', message='Sorry, but please enter a valid pasword.', code=400)

        check_account = _check_credentials(email, password)

        if check_account == False or check_account == None:
            return error(title='Invalid Credentials', message='Sorry, but please enter valid credentials.', code=401)
        else:
            return render_template('portal.html.j2', email=email, account=check_account)

    except Exception as e:
        print(e)
        return error(title='Unknown Error', message='Sorry, but please go back and try again.', code=400)

    return render_template('portal.html.j2')

# /world
@app.route('/world')
def world():
    return render_template('world.html.j2')

# Main page - /
@app.route('/')
def index():
    return render_template('index.html.j2')
