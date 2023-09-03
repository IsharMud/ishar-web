from django.views.generic.base import TemplateView

from ishar.apps.player.models.classes import PlayerClass
from ishar.apps.player.models.race import Race


class FAQView(TemplateView):
    template_name = "faq.html.djt"

    # Fetch/format, links to each playable class with descriptions
    player_classes = [
        f"{pclass.class_display} -- {pclass.class_description}"
        for pclass in PlayerClass.objects.exclude(
            class_description__isnull=True
        ).all()
    ]

    # Fetch, and format, playable player races and descriptions
    player_races = [
        f"{player_race.display_name} -- {player_race.description}"
        for player_race in Race.objects.exclude(
            is_playable=0
        ).all()
    ]

    all_faqs = {

        'Is Ishar MUD free?': [
            '<strong>Yes</strong>! While you are welcome to offer support</a>, '
            'Ishar MUD is free to use, play, and enjoy.'
        ],

        'Are there player classes?': [
            '>Yes! There are '
            f'{len(player_classes)} classes available '
            'to choose from, when you create a player character:',
            player_classes
        ],

        'Are there player races?': [
            'Yes! There are '
            f'{len(player_races)} races available '
            'to choose from, when you create a player character:',
            player_races
        ],

        'Is there role-playing?': [
            '<strong>No</strong>, Ishar MUD does not require role-playing.'
        ],

        'What about my equipment when I log out?': [
            "When you sign out or log off, your character's equipment, gear, "
            'and inventory is simply <strong>preserved until the end of the '
            'season</strong>.', 'The season currently changes every four (4) '
            'months. You can find more information about seasons at the '
            'patches page</a>.'
        ],

        'Is death permanent?': [
            '<strong>You can choose</strong> your game type '
            '(either Classic, or Survival mode) each time that '
            'you create a new player character!',
            'While survival mode gains experience faster, '
            'classic mode subtracts experience upon death, '
            "but allows you to retrieve your character's corpse."
        ],

        'Can I have multiple characters or multi-play?': [
            'You can have up to <strong>ten (10) player characters</strong> '
            'per account!', 'You may actively Mutliplay three (3) characters '
            'at once.', 'Only one account is allowed per person!'
        ],

        'Is there player-killing (PK) or player-versus-player (PvP) combat?': [
            'Yes and no</a>.',
            "While player-versus-player combat (or PK'ing) is possible, "
            'it is very rare, and not a requirement of the game.'
        ]
    }

    extra_context = {"faqs": all_faqs}
