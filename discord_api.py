"""Discord API bot interactions"""
import logging
import requests
from flask import abort, Blueprint, jsonify, request
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from database import db_session
import discord_secret
from models import Season
from sentry import sentry_sdk


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
)


@discord_api.before_request
def before_request():
    """Only accept JSON"""
    if not request.is_json:
        abort(400, 'Invalid request type')

    """Validate Discord request signature"""
    verify_key = VerifyKey(bytes.fromhex(
            discord_secret.PUBLIC_KEY
        )
    )
    signature = request.headers['X-Signature-Ed25519']
    timestamp = request.headers['X-Signature-Timestamp']
    body = request.data.decode('utf-8')

    try:
        verify_key.verify(
            f'{timestamp}{body}'.encode(),
            bytes.fromhex(signature)
        )
    except BadSignatureError:
        abort(401, 'Invalid request signature')


base_url = 'https://discord.com/api/v10/' \
      f'applications/{discord_secret.APPLICATION_ID}/' \
      f'guilds/{discord_secret.GUILD}/commands'
headers = { 'Authorization': f'Bearer {discord_secret.TOKEN}' }

season_cmd = {
    'name': 'season',
    'type': 1,
    'description': 'Show the current Ishar MUD season',
}
r = requests.post(
    url=f"{base_url}/{season_cmd['name']}",
    headers=headers,
    json=jsonify(season_cmd)
)
print(r.content)


@discord_api.route('/discord/api/interactions/', methods=['POST'])
@discord_api.route('/discord/api/interactions', methods=['POST'])
def interactions():
    """Pong"""
    print(request.json)
    print('---')

    if request.json['type'] == 1:
        return respond(
            response={
                'type': 1
            }
        )

    return respond()


def respond(response=None, text=None):
    """Create and return a JSON response,
        for the Discord API HTTPS request"""

    if response:
        logging.info(
            'Response:\n%s',
            response
        )
        return jsonify(
            response
        )

    if not text:
        text = 'Sorry, but IsharMUD Discord bot is under construction!'


    logging.info(
        'Text:\n%s',
        text
    )
    return jsonify(
        {
            'type': 4,
            'data':
            {
                'tts': False,
                'content': text,
                'ephemeral': True,
                'embeds': [],
                'allowed_mentions':
                {
                    'parse': []
                }
            }
        }
    )
