from flask import url_for
faqs = {

    'Is Ishar MUD free?': [
        '<strong>Yes!</strong>',
        'While you are more than welcome to ' \
        '<a href="' + url_for('support') + '" title="Support">offer support</a>, Ishar MUD is free to use, play, and enjoy.'
    ],

    'Are there player classes?': [
        '<strong>Yes!</strong>',
        'There are <strong>five (5)</strong> player classes:',
        [
            'Warrior -- For those who seek to master the art of war.',
            'Rogue -- Sly and cunning, skilled in all things sublime.',
            'Cleric -- The followers of the spirits, both good and evil.',
            'Magician -- Practitioners of the mystic arts, masters of magic.',
            'Necromancer -- Practitioners of necromancy, masters of the undead.',
        ]
    ],

    'Is there role-playing?': [
        '<strong>No.</strong>',
        'Ishar MUD does not require role-playing.'
    ],

    'What about my equipment when I log out?': [
        "When you sign out or log off, your character's equipment, gear, " \
        'and inventory is simply <strong>preserved until the end of the season</strong>.',
        'The season currently changes every four (4) months, but you can find more information about seasons at the latest ' \
        '<a href="' + url_for('static', filename='Major_Update.pdf') + '" title="Major Update" target="_blank">major update</a>.'
    ],

    'Is death permanent?': [
        '<strong>You can choose</strong> whether to play in "Survival" (aka "perma-death") ' \
        'or "Classic" mode, each time you create a player character.',
        'While survival mode gains experience faster, classic mode subtracts experience upon death, ' \
        "but allows you to retrieve your character's corpse."
    ],

    'Can I have multiple characters or multi-play?': [
        '<strong>You can have up to ten (10) player characters</strong> per account!',
        'You may actively <strong>multi-play up to three (3) player characters at once</strong>.',
        'Only one account is allowed!'
    ],

    'Is there player-killing (PK) or player-versus-player (PvP) combat?': [
        '<strong>Yes and no...</strong>',
        "While player-versus-player combat (or PK'ing) is possible, it is very rare, and not a requirement of the game."
    ],

#    'What is your next question?': [
#        '<strong>Bueller?</strong>',
#        'Bueller..?',
#        "Bueller's not here!"
#    ]

}
