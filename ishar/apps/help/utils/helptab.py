from django.conf import settings
from django.urls import reverse
from logging import getLogger
from pathlib import Path
import re

from ..utils.parse import parse_player_class, parse_stats


logger = getLogger(__name__)

# Example from MUD "helptab" file:
"""
<level>
[<state flags 1>] <topic name 1>
...
[<state flags n>] <topic name n>
*
<text of help entry>
[%%<level A>]
<more text for level A and higher>
...
[%%<level X>]
<more text for level X and higher>
#
"""
START_STRING = (
    "###########################"
    "---BEGIN HELP FILE---"
    "###########################\n"
)

# Compile regular expression to parse "see also" items from a help topic.
SEE_ALSO_REGEX = re.compile(
    pattern=(
        r"^(see also|also see|also see help on|see help on|related)\s*\:"
        r"\s*(?P<topics>.+)$"
    ),
    flags=re.IGNORECASE
)

# Compile regular expression to match sections for another level in content.
DIFF_LEVEL_REGEX = re.compile("^\%\%(?P<diff_level>[0-9]{1,2})$")

# Compile regular expressions for help command minimum and syntax.
MINIMUM_REGEX = re.compile(r"^(Minimum|minimum|Min|min)\s*\:\s*(?P<min>.+)$")
SYNTAX_REGEX = re.compile(r"^(Syntax|syntax)\s*\:\s*(?P<syntax>.+)$")

# Compile regular expression for saves, player classes, and components.
SAVE_REGEX = re.compile(r"^Save\s+:\s+(?P<save>.+)$")
PLAYER_CLASS_REGEX = re.compile(r"^Class(es)?\s*\:\s*(?P<pclass>.+)")
COMPONENT_REGEX = re.compile(r"^Components?\s*\:\s*(?P<component>.+)$")

# Compile regular expression for player level in help topic body.
PLAYER_LEVEL_REGEX = re.compile(r"^Level\s*\:\s*(?P<level>.+)$")

# Compile regular expressions to hyperlink body text "`help " references.
HELP_CMD_REGEX = {
    "PATTERN": r"`help ([\w| ]+)'",
    "SUB": r'`<a href="/help/\1\#topic" title="Help: \1">help \1</a>`'
}


def _discover_help(path: Path = settings.HELPTAB) -> list:
    """Discover sections within "helptab" file."""
    # Open the "helptab" file (read-only), and gather its entire contents.
    with open(file=path, mode="r", encoding="utf-8") as helptab_fh:
        helptab_fo = helptab_fh.read()

    # Sections in "helptab" file are separated by "#" on a line alone.
    return helptab_fo.split(START_STRING)[1].split("\n#\n")


class HelpTab:
    """
    Interact with the "helptab" file to find sections representing help topics.
    """
    help_topics: dict = {}
    path: Path = settings.HELPTAB

    def __init__(self, path: (Path, str) = settings.HELPTAB):
        """Discover, and parse, help topics from "helptab" file sections."""
        if path and isinstance(path, str):
            path = Path(path)
            self.path = path
        self.help_topics = self.parse(_discover_help(path=self.path))

    def __repr__(self) -> str:
        """Show the object type with absolute path and topic count string."""
        return f"<{self.__class__.__name__}> {self.__str__()}"

    def __str__(self) -> str:
        """Show absolute path of "helptab" file with number of help topics."""
        return f"{self.path.absolute()} ({len(self.help_topics)} topics)"


    class HelpTopic:
        """
        Help topic from "helptab" file.
        """
        name: str = ""
        level: int = 0
        aliases: set = {}
        body: str = ""
        see_also: set = {}
        syntax: str = ""
        minimum: str = ""
        player_level: (int, str, None) = None
        player_class: (list, str) = []
        save: str = ""
        stats: list = []
        components: list = []

        def __init__(self):
            """Initialization of a "help topic" object."""
            self.name = ""
            self.level = 0
            self.aliases = set()
            self.body = ""
            self.see_also = set()
            self.syntax = ""
            self.minimum = ""
            self.player_level = None
            self.player_class = []
            self.save = ""
            self.stats = []
            self.components = []

        def get_absolute_url(self):
            """Admin link for account upgrade."""
            return reverse(viewname="help_page", args=(self.name,)) + "#topic"

        def parse_header(self, header_lines: list):
            """Parse header of a "helptab" section, to gather aliases."""
            for header_line in header_lines:
                if header_line.startswith("32 "):
                    self.aliases.add(
                        " ".join(header_line.split(" ")[1:]).strip()
                    )

        def parse_content_line(self, content_line: str):
            """Parse single line from the content of a help section."""

            # Check whether the line is for a player level.
            if self.player_level is None:
                lvl_match = PLAYER_LEVEL_REGEX.fullmatch(string=content_line)
                if lvl_match:
                    player_level = lvl_match.group("level")

                    # If player level is numeric, set as integer.
                    self.player_level = player_level
                    if self.player_level.isnumeric():
                        self.player_level = int(self.player_level)

                    return False

            # Check whether the line is for syntax, parsing if so.
            if not self.syntax:
                syntax_match = SYNTAX_REGEX.fullmatch(string=content_line)
                if syntax_match:
                    self.syntax = syntax_match.group("syntax")
                    return False

            # Check whether the line is for minimum, parsing if so.
            if not self.minimum:
                minimum_match = MINIMUM_REGEX.fullmatch(string=content_line)
                if minimum_match:
                    self.minimum = minimum_match.group("min")
                    return False

            # Check whether the line is for player class, parsing if so.
            if not self.player_class and content_line.startswith("Class"):
                pcls_match = PLAYER_CLASS_REGEX.fullmatch(string=content_line)
                if pcls_match:
                    self.player_class = parse_player_class(
                        pcls=pcls_match.group("pclass")
                    )
                    return False

            # Check whether the line is for "Save ", parsing if so.
            if not self.save and content_line.startswith("Save "):
                save_match = SAVE_REGEX.fullmatch(string=content_line)
                if save_match:
                    save_matched = save_match.group("save").strip()
                    if save_matched:
                        self.save = save_matched
                        return False

            # Check whether the line is for "Stats  : ", parsing if so.
            if not self.stats and content_line.startswith("Stats  : "):
                self.stats = parse_stats(line=content_line)
                return False

            # Check whether the line is for components, parsing if so.
            if not self.components and content_line.startswith("Component"):
                component_match = COMPONENT_REGEX.fullmatch(string=content_line)
                self.components = component_match.group("component").split(", ")
                return False

            # Finally, consider the line body text.
            return True


        def parse_content(self, content: str):
            """Parse the content (below "*") of a "helptab" section."""

            # Prepare for parsing any "See also" lines.
            is_see_also = False
            do_skip = False
            also_topics = ""

            # Iterate each line of the help topic content.
            for content_line in content.split("\n"):

                # Handle specific level numbers (%%<##> where ## is the level).
                diff_level_match = DIFF_LEVEL_REGEX.fullmatch(content_line)
                if diff_level_match:

                    # Ignore immortal level sections.
                    diff_level = int(diff_level_match.group("diff_level"))
                    if diff_level >= settings.MIN_IMMORTAL_LEVEL:
                        do_skip = True
                    else:
                        do_skip = False

                    # Skip to the next line.
                    continue

                # Parse line if not otherwise being skipped.
                if do_skip is False:

                    # Look for any "see also" topics, if there are none.
                    if not self.see_also:

                        # Consider text after "see also" to be topic names.
                        also_match = SEE_ALSO_REGEX.fullmatch(content_line)
                        if also_match:
                            is_see_also = True

                        # Add all "see also" topics to long string to be parsed.
                        if is_see_also:
                            if also_match:
                                also_topics = also_match.group("topics")
                            else:
                                also_topics += content_line

                            # Skip to the next line.
                            continue

                    # Parse line as body text.
                    parsed = self.parse_content_line(content_line=content_line)
                    if parsed is True:
                        self.body += f"{content_line}\n"

            # Replace line breaks with a comma in the "see also" topics string.
            also_topics = also_topics.replace("\n", ",")

            # Parse discovered "see also" help topic, adding them to a set.
            if also_topics:
                for also_topic in also_topics.split(","):
                    also_topic = also_topic.strip()
                    if also_topic:
                        self.see_also.add(also_topic)

        @property
        def is_area(self) -> bool:
            """Boolean whether the help topic is an "Area "."""
            if self.name.startswith("Area "):
                return True
            return False

        @property
        def is_spell(self) -> bool:
            """Boolean whether the help topic is a "Spell "."""
            if self.name.startswith("Spell "):
                return True
            return False

        @property
        def body_html(self) -> str:
            """Return body text with links, formatted for HTML display."""

            # Replace HTML tags in body text.
            body = self.body
            for (old, new) in ((">", "g"), ("<", "l")):
                body = body.replace(old, f"&{new}t;")

            # Hyperlink "`help command'" in text within body text.
            body = re.sub(
                pattern=HELP_CMD_REGEX["PATTERN"],
                repl=HELP_CMD_REGEX["SUB"],
                string=body,
                flags=re.MULTILINE
            )
            return body

        def alias_count(self) -> int:
            """Count of number of help topic aliases."""
            return len(self.aliases)

        def pluralize(self, item="alias"):
            """Pluralize "alias", depending upon count of alias(es)."""
            if self.alias_count() == 1:
                return item
            return f"{item}es"

        def __repr__(self) -> str:
            """Show object type with name string."""
            return f"<{self.__class__.__name__}> {self.__str__()}"

        def __str__(self) -> str:
            """Show name of the help topic."""
            return self.name

        def __gt__(self, other):
            return self.name > other.name

        def __lt__(self, other):
            return self.name < other.name

    def parse(self, sections: list) -> dict:
        """Parse "helptab" sections into dictionary of help topic objects."""
        topics = {}

        # Iterate each "helptab" section in the list provided.
        for section in sections:

            # Sections contain a header, and a body, separated by "*".
            try:
                header, content = section.split("\n*\n")

            # Log any skipped "helptab" sections which could not be split.
            except ValueError as val_err:
                logger.error(f"Skipping: {section.__repr__()}")
                logger.exception(val_err)
                continue # Next section.

            # Start with fresh topic to possibly add to returned list later.
            finally:
                help_topic = None

            # First header line is player level to which the section applies.
            header_lines = header.split("\n")
            topic_level = int(header_lines[0])

            # Only consider helptab sections that are meant for mortal players.
            if topic_level < settings.MIN_IMMORTAL_LEVEL:

                # Only consider helptab sections for "32 " ("Playing") state.
                first_line = header_lines[1].strip()
                if first_line.startswith("32 "):

                    # Use anything after first space (after "32 ") as name.
                    name = " ".join(first_line.split(" ")[1:]).strip()

                    # Create a help topic object using the level and name.
                    help_topic = self.HelpTopic()
                    help_topic.level = topic_level
                    help_topic.name = name

                    # Parse the rest of the help topic header, to get aliases.
                    help_topic.parse_header(header_lines=header_lines[2:])

                    # Parse the content (below "*") within the topic section.
                    help_topic.parse_content(content=content)

            # Append newly created help topic object to list of help topics.
            if help_topic is not None and help_topic.name:
                topics[help_topic.name] = help_topic

        # Return complete list of help topics parsed from "helptab" sections.
        return topics


    def search(self, search_name: str) -> dict[str: HelpTopic,]:
        """Search help topic names and aliases for a string."""

        # Immediately return exact match.
        if search_name in self.help_topics:
            return {search_name: self.help_topics[search_name]}

        # Set a variety of formats of the search string.
        fmts = (search_name.title(), search_name.lower(),search_name.upper(),
                search_name.strip(),)

        # Iterate each help topic object to search their names and aliases.
        search_results = {}
        for topic_name, topic in self.help_topics.items():

            # Iterate variety of formats of the string.
            do_add = False
            for name_fmt in fmts:

                # Check if the topic name contains the string.
                if name_fmt in topic_name:
                    do_add = True

                # Check for any alias exact matches.
                elif name_fmt in topic.aliases:
                    do_add = True

                # Check if the topic aliases contain the string.
                else:
                    for alias in topic.aliases:
                        if name_fmt in alias:
                            do_add = True

            #  Add the help topic to the search results, if necessary.
            if do_add is True:
                search_results[topic_name] = topic

        # Return the dictionary of any found help topics.
        return search_results
