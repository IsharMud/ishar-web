"""
Frequently Asked Questions
"""
from flask import url_for
faqs = {

    'Is Ishar MUD free?': [
        '<strong>Yes</strong>! While you are more than welcome to ' \
        '<a href="' + url_for('support') + '" title="Support">offer support</a>, ' \
        'Ishar MUD is free to use, play, and enjoy.'
    ],

    'Are there player classes?': [
        '<strong>Yes</strong>! ' \
        'There are <strong>five (5)</strong> classes available to choose from, ' \
        'when you create a player character:',
        [
            'Warrior -- For those who seek to master the art of war.',
            'Rogue -- Sly and cunning, skilled in all things sublime.',
            'Cleric -- The followers of the spirits, both good and evil.',
            'Magician -- Practitioners of the mystic arts, masters of magic.',
            'Necromancer -- Practitioners of necromancy, masters of the undead.',
        ]
    ],

    'Are there player races?': [
        '<strong>Yes</strong>! ' \
        'There are <strong>six (6)</strong> races available to choose from, ' \
        'when you create a player character:',
        [
            'Human -- The dominant race around Mareldja, the home city.',
            'Elf -- Tall, pointy-eared types.',
            'Dwarf -- Short and hairy.',
            'Hobbit -- Small, magically inclined creatures of the forest.',
            'Gnome -- Small, compactly built mountain and forest dwellers.',
            'Half-Elven -- Crossbreed, of Human and Elven descent.'
        ]
    ],

    'Is there role-playing?': [
        '<strong>No</strong>, ' \
        'Ishar MUD does not require role-playing.'
    ],

    'What about my equipment when I log out?': [
        "When you sign out or log off, your character's equipment, gear, " \
        'and inventory is simply <strong>preserved until the end of the season</strong>.',
        'The <a href="' + url_for('season') + '" title="Season">season</a> currently changes every four (4) months.',
        'You can find more information about seasons at the ' \
        '<a href="' + url_for('latest_patch') + '" title="Patches">latest patch</a> page.'
    ],

    'Is death permanent?': [
        '<strong>You can choose</strong> whether to play in "Survival" (aka "perma-death") ' \
        'or "Classic" mode, each time you create a player character.',
        'While survival mode gains experience faster, classic mode subtracts experience ' \
        "upon death, but allows you to retrieve your character's corpse."
    ],

    'Can I have multiple characters or multi-play?': [
        'You can have up to <strong>ten (10) player characters</strong> per account!',
        'You may actively <strong>multi-play three (3) player characters</strong> at once.',
        'Only one account is allowed per person!'
    ],

    'Is there player-killing (PK) or player-versus-player (PvP) combat?': [
        '<strong>Yes and no</strong>... ' \
        "While player-versus-player combat (or PK'ing) is possible, " \
        'it is very rare, and not a requirement of the game.'
    ],

#    'What is your next question?': [
#        '<strong>Bueller?</strong>',
#        'Bueller..?',
#        "Bueller's not here!"
#    ]

}
