#!/usr/bin/python3
from logging import getLogger
from pathlib import Path
import re

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
logger = getLogger(__name__)

# Specify "helptab" file, minimum "Immortal" level, player class names, etc.
HELPTAB_FILE = Path(Path(__file__).parent, "helptab")
MIN_IMMORTAL_LEVEL = 21
PLAYER_CLASS_NAMES = (
    "Warrior", "Necromancer", "Mage", "Magician", "Shaman", "Cleric", "Rogue",
    "Monk",
)
START_STRING = ("###########################"
                "---BEGIN HELP FILE---###########################\n")

# Compile regular expression to parse "see also" items from a help topic.
SEE_ALSO = r'^ *(see also|also see|also see help on|see help on|related) *\: *'
SEE_ALSO_REGEX = re.compile(pattern=SEE_ALSO, flags=re.IGNORECASE)

# Compile regular expressions for items in help topic contents (below "*").
BODY_REGEXES = {
    "syntax": re.compile(r'^ *(Syntax|syntax) *\: *(.+)$'),
    "minimum": re.compile(r'^ *(Minimum|minimum|Min|min) *\: *(.+)$'),
    "player_level": re.compile(r'^ *(Level|level) *\: *(.+)$'),
    "player_class": re.compile(r'^ *(Class|Classes) *\: *(.+)$'),
    "components": re.compile(r'^ *(Components?) *\: *(.+)$'),
    "saves": re.compile(r'^ *(Saves?) *\: *(.+)$'),
    "stats": re.compile(r'^ *(Stats?) *\: *(.+)$'),
    "topic": re.compile(r'^ *(Topic) *\: *(.+)$')
}

# Compile regular expressions to hyperlink inline body text "`help " references.
HELP_CMD_REGEX = {
    "PATTERN": r"`help ([\w| ]+)'",
    "SUB": r'`<a href="/help/\1" title="Help: \1">help \1</a>`'
}


class HelpTab:
    """
    Interact with the "helptab" file to find sections representing help topics.
    """
    file: Path = HELPTAB_FILE
    help_topics: dict = {}

    def __init__(self):
        """Discover, and parse, help topics from "helptab" file sections."""
        self.help_topics = self.parse(self.discover())

    def topic_count(self) -> int:
        """Number of help topics found in the "helptab" file."""
        return len(self.help_topics)

    def __repr__(self) -> str:
        """Number of help topics and "helptab" file path."""
        return self.__str__()

    def __str__(self) -> str:
        """Number of help topics and "helptab" file path."""
        return (f"{self.__class__.__name__}: {self.topic_count()} topics"
                f" ({self.file.absolute()})")


    class HelpTopic:
        """
        Help topic from "helptab" file.
        """
        name: str = ""
        level: int = 0
        aliases: list = []
        body: str = ""
        body_html: str = ""
        body_text: str = ""
        see_also: list = []

        def __init__(self):
            """Initialization of a "help topic" object."""
            self.name: str = ""
            self.level: int = 0
            self.aliases: list = []
            self.body_html: str = ""
            self.body_text: str = ""
            self.see_also: list = []

            # Default empty strings for potential body attributes.
            for body_item, body_regex in BODY_REGEXES.items():
                self.__setattr__(body_item, "")

        def parse_header(self, header_lines: list):
            """Parse header of a "helptab" section, to gather aliases."""
            for header_line in header_lines:
                if header_line.startswith("32 "):
                    self.aliases.append(
                        " ".join(header_line.split(" ")[1:]).strip()
                    )

        def parse_content(self, content: str):
            """Parse the content (below "*") of a "helptab" section."""

            # Initialize default "see also" (related topic) variables.
            comma_space = ", "
            see_also_text = "See Also: "
            _is_see_also = False

            # Iterate each line of the help topic content.
            for content_line in content.split('\n'):

                # Check if the line is "see also" (related topic) text.
                if SEE_ALSO_REGEX.match(content_line):
                    self.body_html += see_also_text
                    self.body_text += see_also_text
                    _is_see_also = True

                    # Split, format, and count related topics to hyperlink.
                    i = 0
                    rm_begin = content_line.split(':')
                    related_topics = rm_begin[-1].strip().split(',')
                    num_related = len(related_topics)

                    # Iterate any related topics to hyperlink them.
                    for related_topic in related_topics:
                        i += 1
                        if related_topic and related_topic.strip() != '':
                            self.body_html += (
                                f'<a href="/help/{related_topic.strip()}"'
                                f' title="Help: {related_topic.strip()}">'
                                f'{related_topic.strip()}</a>'
                            )
                            self.body_text += related_topic.strip()
                            self.see_also.append(related_topic.strip())

                            # Comma-separate related help topics, except last.
                            if i != num_related:
                                self.body_html += comma_space
                                self.body_text += comma_space
                            else:
                                _is_see_also = False

                # Parse anything else as if it is the body.
                else:

                    # Remove HTML tags from the body line.
                    body_line = content_line
                    for (old, new) in ((">", "g"), ("<", "l")):
                        body_line = body_line.replace(old, f"&{new}t;")

                    # Iterate "body" regular expressions for useful attributes.
                    body_match = None
                    for body_item, body_regex in BODY_REGEXES.items():
                        body_find = body_regex.findall(string=body_line)

                        # Set attributes for any matching items from the body.
                        if body_find and body_find[0]:
                            body_match = body_find[0]
                            self.__setattr__(body_item, body_match[1])

                    # Set formatted text for each body, if no match.
                    if body_match is None:
                        self.body_text += f"{content_line}\n"
                        self.body_html += f"{body_line}<br>\n"

            # Hyperlink "`help command'" inline text within body HTML.
            self.body_html = re.sub(
                pattern=HELP_CMD_REGEX["PATTERN"], repl=HELP_CMD_REGEX["SUB"],
                string=self.body_html, flags=re.MULTILINE
            )

        def alias_count(self) -> int:
            """Count of number of help topic aliases."""
            return len(self.aliases)

        def pluralize(self, item="alias"):
            """Pluralize "alias", depending upon count of alias(es)."""
            if self.alias_count() == 1:
                return item
            return f"{item}es"

        def __repr__(self) -> str:
            """Show the object type with name string, level, and alias count."""
            return f"{self.__class__.__name__}: {self.__str__()}"

        def __str__(self) -> str:
            """Show the name string, level, and alias count."""
            return (
                f"{self.name.__repr__()} (Level {self.level}) "
                f"[{self.alias_count()} {self.pluralize()}]"
            )

    def discover(self) -> list:
        """Discover sections within "helptab" file."""
        # Open the "helptab" file (read-only), and gather its entire contents.
        with open(file=self.file, mode="r", encoding="utf-8") as helptab_fh:
            helptab_fo = helptab_fh.read()

        # Sections in "helptab" file are separated by "#" on a line alone.
        return helptab_fo.split(START_STRING)[1].split("\n#\n")

    def parse(self, sections: list) -> dict:
        """Parse "helptab" sections into dictionary of help topic objects."""
        help_topics = {}

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
            if topic_level < MIN_IMMORTAL_LEVEL:

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
                help_topics[help_topic.name] = help_topic

        # Return complete list of help topics parsed from "helptab" sections.
        return help_topics
