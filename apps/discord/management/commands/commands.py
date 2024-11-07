import requests
import yaml
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
from pprint import pformat


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

        with open(
            file=Path(Path(__file__).parent, "commands.yaml"),
            mode="r",
            encoding="utf-8"
        ) as cmd_yml:
            all_commands = yaml.safe_load(cmd_yml)

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
