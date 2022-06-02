import secrets
from flask import Flask, url_for, render_template

app = Flask(__name__)

@app.route('/clients')
def clients():
    return render_template('clients.html.j2')

@app.route('/')
def index():
    return render_template('index.html.j2', discord_link=secrets.discord_invite_link)
