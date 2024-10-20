import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from pprint import pformat

from apps.players.models.game_type import GameType


class Command(BaseCommand):
    """Get Discord bot commands."""

    help = "Get Discord bot commands."

    def handle(self, *args, **options):

        discord_url = (
            f"https://discord.com/api/v10/applications/"
            f'{settings.DISCORD["APPLICATION_ID"]}/guilds/'
            f'{settings.DISCORD["GUILD"]}/commands'
        )
        discord_headers = {
            "Authorization": f'Bot {settings.DISCORD["TOKEN"]}',
            "Content-Type": "application/json",
            "User-agent": (
                f"{settings.WEBSITE_TITLE} Discord Bot"
                " / https://github.com/IsharMud/ishar-web/"
            ),
        }

        req = requests.get(url=discord_url, headers=discord_headers)
        if req.status_code >= 400:
            self.stdout.write(self.style.ERROR("Bad response."))
            self.stdout.write(
                self.style.ERROR(
                    f"{pformat(req)}:\n"
                    f"{pformat(req.json())}"
                )
            )
            raise CommandError(pformat(req.reason))

        self.stdout.write(
            self.style.SUCCESS(
                f"{pformat(req)}:\n"
                f"{pformat(req.json())}"
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
                "name": "cycle",
                "description": "Show when challenges will cycle next.",
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
                "name": "feedback",
                "description":
                    "Link to feedback page to send bug report,"
                    " idea, or suggestion.",
            },
            {
                "name": "leader",
                "type": 1,
                "description": "List the leading player, by game type.",
                "options": [{
                    "name": "type",
                    "description": "Game type to find the leader of.",
                    "type": 3,
                    "required": False,
                    "choices": [
                        {
                            "name": "Classic",
                            "value": str(GameType.CLASSIC.value)
                        },
                        {
                            "name": "Hardcore",
                            "value": str(GameType.HARDCORE.value)
                        },
                        {
                            "name": "Survival",
                            "value": str(GameType.SURVIVAL.value)
                        }
                    ]
                }]
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
                        "required": True,
                    }
                ],
            },
            {
                "type": 1,
                "name": "mudtime",
                "description": "Show current server time.",
            },
            {
                "type": 1,
                "name": "runtime",
                "description": "Show current server runtime.",
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
                        "required": True,
                    }
                ],
            },
            {
                "type": 1,
                "name": "upgrades",
                "description":
                    "Link to available remort upgrades and their renown costs."
            },
        ]

        reg = requests.put(
            url=discord_url,
            headers=discord_headers,
            json=all_commands
        )

        if reg.status_code >= 400:
            self.stdout.write(self.style.ERROR("Bad response."))
            self.stdout.write(
                self.style.ERROR(
                    f"{pformat(reg)}:\n"
                    f"{pformat(reg.json())}"
                )
            )
            raise CommandError(pformat(reg.reason))

        self.stdout.write(
            self.style.SUCCESS(
                f"{pformat(reg)}:\n"
                f"{pformat(reg.json())}"
            )
        )
