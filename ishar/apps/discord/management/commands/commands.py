import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from pprint import pformat


class Command(BaseCommand):
    """Get Discord bot commands."""

    help = "Get Discord bot commands."

    def handle(self, *args, **options):

        discord_url = (
            "https://discord.com/api/v10/applications/%s/guilds/%s/commands" % (
                settings.DISCORD["APPLICATION_ID"], settings.DISCORD["GUILD"]
            )
        )
        discord_headers = {
            "Authorization": "Bot %s" % (settings.DISCORD["TOKEN"]),
            "Content-Type": "application/json",
            "User-agent": (
                "IsharMUD Discord Bot / https://github.com/IsharMud/ishar-web/"
            ),
        }

        req = requests.get(url=discord_url, headers=discord_headers)
        if req.status_code >= 400:
            self.stdout.write(self.style.ERROR("Bad response."))
            self.stdout.write(
                self.style.ERROR(
                    "%s:\n%s" % (pformat(req), pformat(req.json()))
                )
            )
            raise CommandError(pformat(req.reason))

        self.stdout.write(
            self.style.SUCCESS(
                "%s:\n%s" % (pformat(req), pformat(req.json()))
            )
        )

        all_commands = [
            {
                "type": 1,
                "name": "challenges",
                "description": "Link to the list of MUD challenges.",
            },
            {
                "type": 1,
                "name": "deadhead",
                "description": "Show the player with the most deaths.",
            },
            {
                "type": 1,
                "name": "events",
                "description": "Show any active events.",
            },
            {
                "type": 1,
                "name": "faq",
                "description": "Link to frequently asked questions (FAQs).",
            },
            {
                "type": 1,
                "name": "leaders",
                "description": "Link to the list of leading MUD players.",
            },
            {
                "type": 1,
                "name": "mudhelp",
                "description": "Search MUD help for a topic.",
                "options": [
                    {
                        "name": "topic",
                        "description": "Name of the help topic to search for.",
                        "type": 3,
                        "required": True
                    }
                ]
            },
            {
                "type": 1,
                "name": "mudtime",
                "description": "Show current server time.",
            },
            {
                "type": 1,
                "name": "season",
                "description": "Show the current season.",
            },
            {
                "type": 1,
                "name": "spell",
                "description": "Search MUD help for a spell.",
                "options": [
                    {
                        "name": "spell",
                        "description": "Name of the spell to search for.",
                        "type": 3,
                        "required": True
                    }
                ]
            },
        ]

        reg = requests.put(
            url=discord_url, headers=discord_headers, json=all_commands
        )

        if reg.status_code >= 400:
            self.stdout.write(self.style.ERROR("Bad response."))
            self.stdout.write(
                self.style.ERROR(
                    "%s:\n%s" % (pformat(reg), pformat(reg.json()))
                )
            )
            raise CommandError(pformat(reg.reason))

        self.stdout.write(
            self.style.SUCCESS(
                "%s:\n%s" % (pformat(reg), pformat(reg.json()))
            )
        )
