"""Discord API bot interactions"""
import logging
from flask import abort, Blueprint, jsonify, request
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

import discord_secret


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %Z'
)


# Flask Blueprint
discord_api = Blueprint(
    'discord_api',
    __name__,
    url_prefix='/discord/api'
)


@discord_api.before_request
def before_request():
    """Validate Discord bot API requests"""

    # Fail, with 400, on non-POST requests
    if not request.method == 'POST':
        abort(400, 'Invalid request method')

    # Fail, with 400, on non-JSON requests
    if not request.is_json:
        abort(400, 'Invalid request body')

    # Check request header signature
    try:
        VerifyKey(
            bytes.fromhex(
                discord_secret.PUBLIC_KEY
            )
        ).verify(
            request.headers['X-Signature-Timestamp'] +
            request.data.decode('utf-8')
            .encode(),
            bytes.fromhex(
                request.headers['X-Signature-Ed25519']
            )
        )

    # Fail, with 401, on bad request header signature
    except BadSignatureError:
        abort(401, 'Invalid request signature')


# Set Discord API URL and headers,
#   to register commands (WIP/TODO)
base_url = 'https://discord.com/api/v10/' \
      f'applications/{discord_secret.APPLICATION_ID}/' \
      f'guilds/{discord_secret.GUILD}/commands'
headers = {
    'Authorization': f'Bearer {discord_secret.TOKEN}'
}


# Respond to HTTPS JSON requests from Discord
@discord_api.route('/discord/api/interactions/', methods=['POST'])
@discord_api.route('/discord/api/interactions', methods=['POST'])
def interactions():
    """Pong"""

    # Reply to "ping" requests from Discord
    if request.json['type'] == 1:
        return jsonify(
            {'type': 1}
        )

    # Otherwise, reply saying "under construction"
    return jsonify(
        {
            'type': 4,
            'data':
            {
                'tts': False,
                'content': 'Sorry, but IsharMUD bot is under construction!',
                'ephemeral': True,
                'embeds': [],
                'allowed_mentions':
                {
                    'parse': []
                }
            }
        }
    )
