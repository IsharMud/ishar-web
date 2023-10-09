"""
isharmud.com FAQs
"""
from django.views.generic import TemplateView
from django.urls import reverse
from django.utils.html import mark_safe


class FAQView(TemplateView):
    template_name = "faq.html.djt"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["faqs"] = {
            "Is Ishar MUD free?":
            (
                mark_safe(
                    "<strong>Yes!</strong> While you are welcome to "
                    '<a href="%s">offer support</a>'
                    ", Ishar MUD is free to use, play, and enjoy." % (
                        reverse(viewname="support")
                    )
                ),
            ),
            "Are there player classes?":
            (
                mark_safe(
                    '<a href="%s">Yes! There are 5 classes</a> available'
                    " to choose from, when you create a player character:" % (
                        reverse(
                            viewname="help_page",
                            kwargs={"help_topic": "Classes"}
                        )
                    )
                ),
                mark_safe(
                    '<a href="%s">Warrior</a> -- '
                    "For those who seek to master the art of war." % (
                        reverse(
                            viewname="help_page",
                            kwargs={"help_topic": "Warrior"}
                        )
                    )
                ),
                mark_safe(
                    '<a href="%s">Rogue</a> -- '
                    "Sly and cunning, skilled in all things sublime." % (
                        reverse(
                            viewname="help_page",
                            kwargs={"help_topic": "Rogue"}
                        )
                    )
                ),
                mark_safe(
                    '<a href="%s">Cleric</a> -- '
                    "The followers of the spirits, both good and evil." % (
                        reverse(
                            viewname="help_page",
                            kwargs={"help_topic": "Cleric"}
                        )
                    )
                ),
                mark_safe(
                    '<a href="%s">Magician</a> -- '
                    "Practitioners of the mystic arts, masters of magic." % (
                        reverse(
                            viewname="help_page",
                            kwargs={"help_topic": "Mage"}
                        )
                    )
                ),
                mark_safe(
                    '<a href="%s">Necromancer</a> -- '
                    "Practitioners of necromancy, masters of the undead." % (
                        reverse(
                            viewname="help_page",
                            kwargs={"help_topic": "Necromancer"}
                        )
                    )
                )
            ),
            "Are there player races?":
            (
                mark_safe(
                    '<a href="%s">Yes! There are 6 races</a> available'
                    " to choose from, when you create a player character:" % (
                        reverse(
                            viewname="help_page",
                            kwargs={"help_topic": "Races"}
                        )
                    )
                ),
                "Human -- appears to be of human origin",
                "Elf -- looks to be of elven descent",
                "Dwarf -- appears dwarvish",
                "Halfling -- seems wizened beyond years, and built stockily"
                "  yet frail",
                "Gnome -- is possessed of gnomish features",
                "Half-Elven -- looks to be of human and elven descent"
            ),
            "Is there role-playing?":
            (
                mark_safe(
                    "<strong>No.</strong>"
                    " Ishar MUD does not require role-playing."
                ),
            ),
            "What about my equipment when I log out?":
            (
                mark_safe(
                    "When you sign out or log off, your character's"
                    " equipment, gear, and inventory is simply "
                    "<strong>preserved until the end of the season.</strong>"
                ),
                mark_safe(
                    'The <a href="%s">season</a> currently'
                    " changes every four (4) months." % (
                        reverse("current_season")
                    ),
                ),
                mark_safe(
                    "You can find more information about seasons at the"
                    ' <a href="%s">patches</a> page.' % (
                        reverse("patches")
                    ),
                )
            ),
            "Is death permanent?":
            (
                mark_safe(
                    "<strong>You can choose</strong> your "
                    '<a href="%s">game type</a>'
                    " (either Classic, or Survival mode)"
                    " each time that you create a new player character!" % (
                        reverse(
                            viewname="help_page",
                            kwargs={"help_topic": "Game Types"}
                        )
                    )
                ),
                "While survival mode gains experience faster,"
                " classic mode subtracts experience upon death,"
                " but allows you to retrieve your character's corpse."
            ),
            "Can I have multiple characters or multi-play?":
            (
                mark_safe(
                    "You can have up to <strong>ten (10) player "
                    "characters</strong> per account!"
                ),
                mark_safe(
                    'You may actively <a href="%s">multi-play</a> three (3)'
                    " characters at once." % (
                        reverse(
                            viewname="help_page",
                            kwargs={"help_topic": "Multiplay"}
                        )
                    )
                ),
                "Only one account is allowed per person!"
            ),
            "Is there player-killing (PK) or player-versus-player"
            " (PvP) combat?":
            (
                mark_safe(
                    '<a href="%s">Yes and no.</a>' % (
                        reverse(
                            viewname="help_page",
                            kwargs={"help_topic": "Player Killing"}
                        )
                    )
                ),
                "While player-versus-player combat (or PK'ing) is possible,"
                " it is rare, and not a requirement of the game."
            )
        }
        return context
