import secrets
from flask import Flask, redirect, render_template, url_for

# Name the "app" (as uwsgi expects)
app = Flask(__name__)

# /clients
@app.route('/clients')
def clients():
    return render_template('clients.html.j2')

# Redirect /connect to mudslinger.net
@app.route('/connect')
def connect():
    return redirect('https://mudslinger.net/play/?host=isharmud.com&port=23', code=302)

# Redirect /discord to the link listed in secrets.py
@app.route('/discord')
def discord():
    return redirect(secrets.discord_invite_link, code=302)

# /help in progress
@app.route('/help')
@app.route('/help/<string:page>')
def help(page=None):
    return render_template('help.html.j2', page=page)

# /world
@app.route('/world')
def world():
    return render_template('world.html.j2')

# Main page - /
@app.route('/')
def index():
    return render_template('index.html.j2')
