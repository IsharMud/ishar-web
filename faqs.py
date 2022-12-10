"""Frequently Asked Questions"""
from flask import Blueprint, render_template, url_for

from models import PlayerClass, PlayerRace

faqs = Blueprint('faqs', __name__)


@faqs.route('/questions/', methods=['GET'])
@faqs.route('/faqs/', methods=['GET'])
@faqs.route('/faq/', methods=['GET'])
@faqs.route('/questions', methods=['GET'])
@faqs.route('/faqs', methods=['GET'])
@faqs.route('/faq', methods=['GET'])
def index():
    """A few frequently asked questions (/faq, /faqs, or /questions)"""

    # Fetch, and format, links to each of the playable player classes with descriptions
    player_classes = [
        f"<a href=\"{url_for('help_page.single', topic=player_class.class_display_name)}\">"
        f"{player_class.class_display_name}</a> -- {player_class.class_description}"
        for player_class in PlayerClass().query.filter(PlayerClass.class_description != '').all()
    ]

    # Fetch, and format, playable player races and descriptions
    player_races = [
        f"{player_race.race_display_name} -- {player_race.race_description}"
        for player_race in PlayerRace().query.filter(PlayerRace.race_description != '').all()
    ]

    all_faqs = {

        'Is Ishar MUD free?': [
            '<strong>Yes</strong>! While you are more than welcome to '
            '<a href="' + url_for('support.index') +
            '" title="Support">offer support</a>, '
            'Ishar MUD is free to use, play, and enjoy.'
        ],

        'Are there player classes?': [
            '<a href="' + url_for('help_page.single', topic='Classes') + '">Yes! '
            f'There are {len(player_classes)} classes</a> available to choose from, ',
            'when you create a player character:',
            player_classes
        ],

        'Are there player races?': [
            '<a href="' + url_for('help_page.single', topic='Races') + '">Yes! '
            f'There are {len(player_races)} races</a> available to choose from, '
            'when you create a player character:',
            player_races
        ],

        'Is there role-playing?': [
            '<strong>No</strong>, '
            'Ishar MUD does not require role-playing.'
        ],

        'What about my equipment when I log out?': [
            "When you sign out or log off, your character's equipment, gear, "
            'and inventory is simply <strong>preserved until the end of the season</strong>.',
            'The <a href="' + url_for('season.index') +
            '" title="Season">season</a> '
            'currently changes every four (4) months.',
            'You can find more information about seasons at the '
            '<a href="' + url_for('patches.index') +
            '" title="Patches">patches</a> page.'
        ],

        'Is death permanent?': [
            '<strong>You can choose</strong> whether to play in "Survival" '
            '(aka &quot;<a href="' + url_for('help_page.single', topic='Permadeath') + '">perma-death</a>&quot;) '
            'or "Classic" mode, each time you create a player character.',
            'While survival mode gains experience faster, classic mode subtracts experience '
            "upon death, but allows you to retrieve your character's corpse."
        ],

        'Can I have multiple characters or multi-play?': [
            'You can have up to <strong>ten (10) player characters</strong> per account!',
            '<a href="' + url_for('help_page.single', topic='Mutliplay') + '">'
            'You may actively multi-play three (3) player characters</strong> at once.</a>',
            'Only one account is allowed per person!'
        ],

        'Is there player-killing (PK) or player-versus-player (PvP) combat?': [
            '<a href="' + url_for('help_page.single', topic='Player Killing') + '">Yes and no.</a>',
            "While player-versus-player combat (or PK'ing) is possible, "
            'it is very rare, and not a requirement of the game.'
        ]
    }

    return render_template('faqs.html.j2', faqs=all_faqs)
