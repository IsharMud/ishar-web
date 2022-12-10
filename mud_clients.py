"""MUD Clients"""
from flask import Blueprint, render_template

mud_clients = Blueprint('mud_clients', __name__)


@mud_clients.route('/mud_clients', methods=['GET'])
@mud_clients.route('/clients', methods=['GET'])
def index():
    """A few popular MUD clients (/clients, or /mud_clients)"""

    all_clients = {

        'Cross-Platform': {
            'Mudlet': 'https://www.mudlet.org/'
        },

        'Android': {
            'Blowtorch': 'http://bt.happygoatstudios.com/'
        },

        'iOS': {
            'MUDRammer': 'https://splinesoft.net/mudrammer/'
        },

        'Linux / UNIX': {
            'TinTin++': 'http://tintin.sourceforge.net/',
            'TinyFugue': 'http://tinyfugue.sourceforge.net/'
        },

        'Mac OS': {
            'Atlantis': 'https://www.riverdark.net/atlantis/',
            'MudWalker': 'http://mudwalker.cubik.org/'
        },

        'Windows': {
            'ZMud': 'https://www.zuggsoft.com/zmud/zmudinfo.htm',
            'alclient': 'https://www.ashavar.com/client/',
            'yTin': 'http://ytin.sourceforge.net/',
            'Gosclient': 'http://gosclient.altervista.org/eng/',
            'MUSHclient': 'https://www.gammon.com.au/downloads/dlmushclient.htm'
        }
    }

    return render_template('mud_clients.html.j2', mud_clients=all_clients)
