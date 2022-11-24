"""Redirects"""
from flask import Blueprint, redirect

redirects = Blueprint('redirects', __name__)

@redirects.route('/connect/', methods=['GET'])
@redirects.route('/connect', methods=['GET'])
def connect():
    """Redirect /connect GET requests to mudslinger.net web client"""
    return redirect('https://mudslinger.net/play/?host=isharmud.com&port=23')


@redirects.route('/discord/', methods=['GET'])
@redirects.route('/discord', methods=['GET'])
def discord():
    """Redirect /discord GET requests to the Discord invitation link"""
    return redirect('https://discord.gg/VBmMXUpeve')
