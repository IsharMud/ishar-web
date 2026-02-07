"""Django management command to sync slash commands with Discord."""

from pathlib import Path
from pprint import pformat

import requests
import yaml
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


COMMANDS_YAML = Path(__file__).parent / "commands.yaml"


class Command(BaseCommand):
    """Sync Discord slash command definitions with the Discord API."""

    help = "Fetch current and register slash commands with the Discord API."

    def _api_url(self) -> str:
        discord = settings.DISCORD
        return (
            f"https://discord.com/api/applications/"
            f'{discord["APPLICATION_ID"]}/guilds/'
            f'{discord["GUILD"]}/commands'
        )

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f'Bot {settings.DISCORD["TOKEN"]}',
            "Content-Type": "application/json",
            "User-Agent": (
                f"{settings.WEBSITE_TITLE} Discord Bot"
                " / https://github.com/IsharMud/ishar-web/"
            ),
        }

    def _check_response(self, resp: requests.Response, label: str) -> None:
        if resp.status_code >= 400:
            detail = pformat(resp.json())
            self.stderr.write(self.style.ERROR(f"{label} failed: {detail}"))
            raise CommandError(resp.reason)
        self.stdout.write(self.style.SUCCESS(f"{label}: {pformat(resp.json())}"))

    def handle(self, *args, **options) -> None:
        url = self._api_url()
        headers = self._headers()

        # Show current registered commands.
        self.stdout.write("Fetching current commands...")
        resp = requests.get(url=url, headers=headers)
        self._check_response(resp, "GET commands")

        # Load desired command definitions from YAML.
        with COMMANDS_YAML.open(encoding="utf-8") as fh:
            all_commands = yaml.safe_load(fh)

        # Bulk-overwrite with the YAML definitions.
        self.stdout.write("Registering commands...")
        resp = requests.put(url=url, headers=headers, json=all_commands)
        self._check_response(resp, "PUT commands")

        self.stdout.write(self.style.SUCCESS("Done."))
