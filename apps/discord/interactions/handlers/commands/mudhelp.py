from django.urls import reverse

from apps.help.utils.helptab import HelpTab

from .base import SlashCommand


class MudhelpCommand(SlashCommand):
    """Search MUD help for a topic."""

    name = "mudhelp"
    ephemeral = True
    option_name = "topic"
    not_found_label = "help topic"

    def handle(self) -> tuple[str, bool]:
        search = self.get_option(self.option_name, "")
        if not search:
            return f"Sorry, no such {self.not_found_label} could be found.", True

        helptab = HelpTab()
        results = helptab.search(search_name=search)
        if not results:
            return f"Sorry, no such {self.not_found_label} could be found.", True

        num_results = len(results)
        if num_results == 1:
            result = next(iter(results.values()))
            label = result.name
            url = f"{self.base_url()}{result.get_absolute_url()}"
        else:
            label = f"{num_results} results"
            path = reverse(viewname="help_page", args=(search,))
            url = f"{self.base_url()}{path}#topics"

        return f":information_source: [{label}](<{url}>)", False


class SpellCommand(MudhelpCommand):
    """Search MUD help for a spell."""

    name = "spell"
    option_name = "spell"
    not_found_label = "spell"
