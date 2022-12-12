"""Discord invite redirect, and bot interactions"""
from flask import Blueprint, jsonify, redirect, request


discord = Blueprint('discord', __name__, url_prefix='/discord')


@discord.route('/interactions', methods=['POST'])
def my_command():
    """My command"""

    if request.json['type'] == 1:
        return jsonify(
            {
                'type': 1
            }
        )

    return jsonify(
        {
            'type': 4,
            'data':
            {
                'tts': False,
                'content': 'Congrats on sending your command!',
                'embeds': [],
                'allowed_mentions':
                {
                    'parse': []
                }
            }
        }
    )


@discord.route('/', methods=['GET'])
def invite():
    """Redirect /discord GET requests to the Discord invite"""
    return redirect('https://discord.gg/VBmMXUpeve')
