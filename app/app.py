import config
import secrets
from flask import Flask, redirect, render_template, request, url_for
import mariadb
import crypt
import hmac

# Name the "app" (as uwsgi expects)
app = Flask(__name__)

# Error handling
def error(title='Page Not Found', message='Hmmm... the page you are looking for can not be found.', code=404):
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
    return error(tite='Internal Server Error', message=message, code=500)

@app.errorhandler(501)
def method_not_implemented(message):
    return error(title='Method Not Implemented', message=message, code=501)

@app.errorhandler(503)
def service_unavailable(message):
    return error(title='Service Unavailable', message=message, code=503)


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
def _check_credentials(user_email, user_password):

    if not user_email or user_email == '':
        return False

    if not user_password or user_password == '':
        return False

    try:
        dbc = _db_connect()
        cur = dbc.cursor()
        cur.execute("SELECT account_id, email, password FROM accounts WHERE email = ?", (user_email,))
        r = cur.fetchall()
        rc = cur.rowcount
        dbc.close()

        # No such account with that e-mail address
        if rc == 0:
            return False

        # Found an account...
        elif rc == 1:

            # Compare password hash
            if hmac.compare_digest(crypt.crypt(user_password, r[0][2]), r[0][2]):
                return r[0][0]

            # Invalid password
            else:
                return False

        # This should not really happen (unless an e-mail is in the database more than once?)
        else:
            return error(title='Duplicate E-mail!', message="Sorry, but please <a href='" + url_for('login_form') + "'>go back</a> and try again.", code=500)

    except Exception as e:
        print(e)
        return error(title='Unknown Error!', message="Sorry, but please <a href='" + url_for('login_form') + "'go back</a> and try again.", code=500)

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

# /help in progress
@app.route('/help')
@app.route('/help/<string:page>')
def help(page=None):
    return render_template('help.html.j2', page=page)

@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html.j2')

# Portal - /portal (after /login)
@app.route('/portal', methods=['GET'])
def portal(account_id=None):

    dbc = _db_connect()
    cur = dbc.cursor()
    cur.execute("SELECT * FROM `accounts` where `account_id` = ?", (account_id,))
    fields = [field_md[0] for field_md in cur.description]
    result = [dict(zip(fields,row)) for row in cur.fetchall()]
    print(result)
    dbc.close()

    return render_template('portal.html.j2', account=result[0])


# POST /login, Process Log In attempt and welcome user
@app.route('/login', methods=['POST'])
def process_login():

    try:
        email =  request.form['email']
        password =  request.form['password']

        if not email or email == '':
            return error(title='Invalid E-mail Address', message="Sorry, but please <a href='" + url_for('login_form') + "'>go back</a> and enter a valid e-mail address.", code=400)

        if not password or password == '':
            return error(title='Invalid Password', message="Sorry, but please <a href='" + url_for('login_form') + "'>go back</a> and enter a valid pasword.", code=400)

        # Check credentials / get account details
        check_account = _check_credentials(email, password)

        # Invalid credentials
        if check_account == False or check_account == None:
            return error(title='Invalid Credentials', message="Sorry, but please <a href='" + url_for('login_form') + "'>go back</a> and enter a valid e-mail address and password.", code=401)

        # Valid credentials! send them to the portal
        elif isinstance(check_account, int):
            return portal(account_id=check_account)
            return render_template('portal.html.j2', account=check_account)

        else:
            raise

    except Exception as e:
        print(e)
        return error(title='Unknown Error', message="Sorry, but please <a href='" + url_for('login_form') + "'>go back</a> and try again.", code=400)

# /world
@app.route('/world')
def world():
    return render_template('world.html.j2')

# Main page - /
@app.route('/')
def index():
    return render_template('index.html.j2')
