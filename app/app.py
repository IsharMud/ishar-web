import config
import secrets
from flask import Flask, make_response, redirect, render_template, request, url_for
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
    return error(title='Internal Server Error', message=message, code=500)

@app.errorhandler(501)
def method_not_implemented(message):
    return error(title='Method Not Implemented', message=message, code=501)

@app.errorhandler(503)
def service_unavailable(message):
    return error(title='Service Unavailable', message=message, code=503)


# Internal function to return account details from the database via account ID
def _get_account(account_id=None, dbc=None):

    if not account_id or account_id == '' or not isinstance(account_id, int):
        return None

    try:
        print(f"_get_account() ...")
        print(f"account_id: {account_id}")

        # Use existing database connection if we can
        if not dbc:
            dbc = _db_connect()
            close_later = True
        else:
            close_later = False

        # Get the account information based on the account ID
        cur = dbc.cursor()
        cur.execute("""SELECT \
                    `account_id`, `email`, `created_at`, `password`, `account_name` \
                    FROM `accounts` \
                    WHERE `account_id` = ?""", (account_id,))
        account_fields = [field_md[0] for field_md in cur.description]
        account = [dict(zip(account_fields,row)) for row in cur.fetchall()]
        print(f"account:\n{account[0]}\n")

        # Close database connection if we made one
        if close_later:
            print(f"Closing database... {dbc}")
            dbc.close()
            print(f"Database closed. {dbc}")

        return account

    except Exception as e:
        print(e)
        return None


# Internal function to return players details from the database via account ID
def _get_players(account_id=None, dbc=None):

    if not account_id or account_id == '' or not isinstance(account_id, int):
        return None

    try:

        print(f"_get_players() ...")
        print(f"account_id: {account_id}")

        # Use existing database connection if we can
        if not dbc:
            dbc = _db_connect()
            close_later = True
        else:
            close_later = False

        # Get the account information based on the account ID
        cur = dbc.cursor()
        cur.execute("""SELECT \
                    `id`, `account_id`, `name`, `level`, \
                    `bankacc`, `renown`, `remorts`, FROM_UNIXTIME(`birth`) as `birth`, \
                    `class_name`, `race_name` \
                    FROM `players` \
                    INNER JOIN `classes` ON `players`.`class_id` = `classes`.`class_id` \
                    INNER JOIN `races` ON `players`.`race_id` = `races`.`race_id` \
                    WHERE `account_id` = ?""", (account_id,))
        players_fields = [field_md[0] for field_md in cur.description]
        players = [dict(zip(players_fields,row)) for row in cur.fetchall()]
        player_count = cur.rowcount
        print(f"player count: {player_count}")

        if player_count == 0:
            players = None

        print(f"players: \n{players}\n")

        return players

    except Exception as E:
        print(e)
        return None


# Internal function to connect to the database
def _db_connect(user=secrets.db_creds['user'], password=secrets.db_creds['password'], host=secrets.db_creds['host'], port=secrets.db_creds['port'], database=secrets.db_creds['database']):

    try:
        print(f"_db_connect() ...")

        # Connect to the database
        conn = mariadb.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )

        # Return the connection
        print(f"Connected to database: {conn}")
        return conn

    except mariadb.Error as e:
        print(e)
        return False

    except Exception as e:
        print(e)
        return False


# Internal function to validate e-mail address and password
# - either with the password hash from the cookies or from the log in form
def _check_credentials(user_email=None, user_password=None, dbc=None):

    if not user_email or user_email == '' or not user_password or user_password == '':
        return None

    try:

        print(f"_check_credentials() ...")
        print(f"user_email: {user_email}")

        # Use existing database connection if we can
        if not dbc:
            dbc = _db_connect()
            close_later = True
        else:
            close_later = False

        # Get basic account information to compare e-mail address and password
        cur = dbc.cursor()
        cur.execute("SELECT `account_id`, `email`, `password` FROM `accounts` WHERE `email` = ?", (user_email,))
        r = cur.fetchall()
        rc = cur.rowcount

        # Close database connection if we made one
        if close_later:
            print(f"Closing database... {dbc}")
            dbc.close()
            print(f"Database closed. {dbc}")

        # No such account with that e-mail address
        if rc == 0:
            print(f"No account found for {user_email}")
            return None

        # Found an account...
        elif rc == 1:

            # Compare directly to database
            # (for cookies, which contain the hashed password value)
            if user_password == r[0][2]:
                print(f"Hash match for {user_email}")
                return r[0][0]

            # Hash and compare to database
            # (for POSTed form values)
            elif hmac.compare_digest(crypt.crypt(user_password, r[0][2]), r[0][2]):
                print(f"Password match for {user_email}")
                return r[0][0]

            # Invalid password
            else:
                print(f"Invalid password for {user_email}")
                return False

        # Duplicate e-mail address in the database should NOT happen
        else:
            print(f"Duplicate e-mail address in database? {user_email}")
            return False

    except Exception as e:
        print(e)
        return None


# GET /password - form to allow a user to change their password
@app.route('/password', methods=['GET'])
def password():

    try:

        # Check authentication / get account ID
        account_id = _check_auth()
        print(f"account_id: {account_id}")
        if not account_id or not isinstance(account_id, int):
            print(f"Invalid account_id ({account_id})")
            raise Exception

        # Get account information from the database
        account = _get_account(account_id=account_id)
        print(f"account name: {account[0]['account_name']}")

        return error(title='Under Construction', message='This page is a work in progress.')

    except Exception as e:
        print(e)
        return error(title='Under Construction', message='This page is a work in progress.')

#        return render_template('password.html.j2', account=account[0])


# POST /password - process password change form
@app.route('/password', methods=['POST'])
def change_password():

    try:

        # Check authentication / get account ID
        print("change_password() ...")
        account_id = _check_auth()
        print(f"account_id: {account_id}")
        if not account_id or not isinstance(account_id, int):
            print(f"Invalid account_id ({account_id})")
            raise Exception

        return error(title='Under Construction', message='This page is a work in progress.')

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


# Redirect /discord to the invite link (in config.py)
@app.route('/discord')
def discord():
    return redirect(config.discord_invite_link, code=302)


# /help - WIP!
@app.route('/help', methods=['GET'])
@app.route('/help/<string:letter>')
@app.route('/help/<string:letter>/')
@app.route('/help/<string:letter>/<string:page>.html')
def help(letter=None, page=None):
    return render_template('help.html.j2', letter=letter, page=page)


# POST /help - help search / WIP!!!
@app.route('/help', methods=['POST'])
def search_help(search_help=None):
    if request.form['search_help'] and request.form['search_help'] != '':
        search_help = request.form['search_help']
        return help(letter=search_help[0], page=search_help)
    else:
        return help()

# Internal function to check for valid authentication
# whether via hash from cookie or POSTed form value
def _check_auth():

    try:
        print(f"_check_auth() ...")

        # Check for cookies
        if request.cookies.get('email') and request.cookies.get('password') and request.cookies.get('email') != '' and request.cookies.get('password') != '':
            email = request.cookies.get('email')
            password = request.cookies.get('password')
            print("Using cookies...")

        # Check for form values
        elif request.form['email'] and request.form['password'] and request.form['email'] != '' and request.form['password'] != '':
            email =  request.form['email']
            password =  request.form['password']
            print("Using form values...")

        else:
            print(f"Got nothing...")
            return None

        # Check credentials
        print(f"Checking credentials... / {email}")
        check_credentials = _check_credentials(email, password)
        print(f"check_credentials: {check_credentials}")
        return check_credentials

    except Exception as e:
        print(e)
        return None


# /login (log in form, or handles cookie login)
@app.route('/login')
def login():
    print("login() ...")
    account_id = _check_auth()
    print(f"account_id: {account_id}")
    if account_id and isinstance(account_id, int):
        print(f"Successful log in for account_id {account_id}")
        return redirect(url_for('portal'), code=302)

    # Otherwise, return log in form
    else:
        print("No authentication, providing form...")
        return render_template('login.html.j2')


# /portal Portal - once logged in
@app.route('/portal', methods=['GET', 'POST'])
def portal():

    try:

        # Check authentication / get account ID
        print(f"portal() ...")
        account_id = _check_auth()
        print(f"account_id: {account_id}")
        if not account_id or not isinstance(account_id, int):
            print(f"Invalid account_id ({account_id})")
            raise Exception

        # Get account and players information
        dbc = _db_connect()
        account = _get_account(account_id=account_id, dbc=dbc)
        players = _get_players(account_id=account_id, dbc=dbc)

        # Close database connection
        print(f"Closing database... {dbc}")
        dbc.close()
        print(f"Database closed. {dbc}")

        # Set cookies of the e-mail address and password hash
        resp = make_response(render_template('portal.html.j2', account=account[0], players=players))
        resp.set_cookie('email', account[0]['email'], secure=True)
        resp.set_cookie('password', account[0]['password'], secure=True)
        return resp

#
#           TODO
#           Deal with player flags
#

#            player_ids = []
#            for player in players:
#                player_ids.append(player['id'])
#            print(f"player ids: {player_ids}")
#            players_idsc = [str(element) for element in player_ids]
#            players_id_numbers = ",".join(players_idsc)
#            print(f"players_id_numbers: {players_id_numbers}")

            # Get player_flags information
#            cur.execute(f"SELECT * FROM `player_player_flags` WHERE `player_id` IN ({players_id_numbers})")
#            players_flags = cur.fetchall()
#            print(f"players_flags: {players_flags}")

    except Exception as e:
        print(e)
        return error(
                        title='Invalid Credentials',
                        message="Sorry, but please <a href='" + url_for('login') + "'>go back</a> and try again.",
                        code=401
                    )


# /logout
@app.route('/logout')
def logout():

    # Set empty cookies for the e-mail address and password hash
    resp = make_response(render_template('error.html.j2', title='Log Out', message='You have been logged out.'))
    resp.set_cookie('email', '', secure=True)
    resp.set_cookie('password', '', secure=True)
    return resp


# /world
@app.route('/world')
def world():
    return render_template('world.html.j2')


# Main page - /
@app.route('/')
def index():
    return render_template('index.html.j2')
