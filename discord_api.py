"""Discord API bot interactions"""
from flask import abort, Blueprint, jsonify, request
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

import discord_secret


discord_api = Blueprint(
    'discord_api',
    __name__,
)


@discord_api.before_request
def before_request():
    """Check/verify Discord request signature"""
    verify_key = VerifyKey(
        bytes.fromhex(discord_secret.PUBLIC_KEY)
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


@discord_api.route('/discord/api/interactions/', methods=['POST'])
@discord_api.route('/discord/api/interactions', methods=['POST'])
def pong():
    """Pong"""
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
                'content': 'Sorry, but Ishar MUD Bot is under construction!',
                'ephemeral': True,
                'embeds': [],
                'allowed_mentions':
                {
                    'parse': []
                }
            }
        }
    )
