"""Base class and registry for Discord slash commands."""

from __future__ import annotations

from logging import getLogger
from typing import Any

from django.http import HttpRequest
from django.urls import reverse


logger = getLogger(__name__)

# Global command registry: {command_name: CommandClass}
_registry: dict[str, type[SlashCommand]] = {}


def get_command(name: str) -> type[SlashCommand] | None:
    """Look up a registered slash command by name."""
    return _registry.get(name)


def get_all_commands() -> dict[str, type[SlashCommand]]:
    """Return a copy of the full command registry."""
    return dict(_registry)


class SlashCommand:
    """Base class for Discord slash commands.

    Subclass this and set ``name`` to register a new command.
    Override ``handle()`` to provide the command logic.

    Class attributes:
        name:      The slash-command name as registered with Discord.
        ephemeral: Whether the response is visible only to the invoking user.
    """

    name: str = ""
    ephemeral: bool = True

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Auto-register concrete subclasses that define a name."""
        super().__init_subclass__(**kwargs)
        if cls.name:
            _registry[cls.name] = cls

    def __init__(
        self,
        request: HttpRequest | None = None,
        interaction_data: dict | None = None,
    ) -> None:
        self.request = request
        self.interaction_data = interaction_data or {}

    # -- helpers available to every command --

    def base_url(self) -> str:
        """Build the site base URL from the current request."""
        if self.request is None:
            return ""
        return f"{self.request.scheme}://{self.request.get_host()}"

    def site_url(self, view_name: str, *args: Any, fragment: str = "") -> str:
        """Build a full site URL for a named Django view."""
        path = reverse(view_name, args=args)
        url = f"{self.base_url()}{path}"
        if fragment:
            url += f"#{fragment}"
        return url

    def site_link(
        self,
        label: str,
        view_name: str,
        *args: Any,
        fragment: str = "",
    ) -> str:
        """Build a Discord-flavoured markdown link to a site page."""
        url = self.site_url(view_name, *args, fragment=fragment)
        return f"[{label}](<{url}>)"

    def get_options(self) -> list[dict]:
        """Return the list of option dicts sent with this interaction."""
        return self.interaction_data.get("options") or []

    def get_option(self, name: str, default: Any = None) -> Any:
        """Return the value of a single named option, or *default*."""
        for opt in self.get_options():
            if opt.get("name") == name:
                return opt.get("value", default)
        return default

    # -- the method subclasses must implement --

    def handle(self) -> tuple[str, bool]:
        """Execute the command and return ``(message, ephemeral)``.

        Subclasses **must** override this method.
        """
        raise NotImplementedError

    # -- public entry point --

    @classmethod
    def execute(
        cls,
        request: HttpRequest | None = None,
        interaction_data: dict | None = None,
    ) -> tuple[str, bool]:
        """Instantiate the command handler and run it."""
        instance = cls(request=request, interaction_data=interaction_data)
        return instance.handle()
