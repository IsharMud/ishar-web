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
SEE_ALSO_REGEX = re.compile(
    pattern=r"^ *(see also|also see|also see help on|see help on|related) *\: "
            r"* (.+)$",
    flags=re.IGNORECASE
)

# Compile regular expressions for items in help topic contents (below "*").
BODY_REGEXES = {
    "syntax": re.compile(pattern=r"^ *(Syntax|syntax) *\: *(.+)$"),
    "minimum": re.compile(pattern=r"^ *(Minimum|minimum|Min|min) *\: *(.+)$"),
    "components": re.compile(pattern=r"^ *(Components?) *\: *(.+)$"),
    "saves": re.compile(pattern=r"^ *(Saves?) *\: *(.+)$"),
    "topic": re.compile(pattern=r"^ *(Topic) *\: *(.+)$")
}

# Compile regular expression for stat in help topic body.
PLAYER_STATS_REGEX = re.compile(pattern=r"^ *(Stats?) *\: *(.+)$")

# Compile regular expressions for player level and class in help topic body.
PLAYER_LEVEL_REGEX = re.compile(pattern=r"^ *(Level|level) *\: *(.+)$")
PLAYER_CLASS_REGEX = re.compile(pattern=r"^ *(Class|Classes) *\: *(.+)$")

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

    @property
    def topics(self) -> dict:
        """Set "topics" property to "help_topics" dictionary."""
        return self.topics

    def __repr__(self) -> str:
        """Show the object type with absolute path and topic count string."""
        return f"<{self.__class__.__name__}> {self.__str__()}"

    def __str__(self) -> str:
        """Show absolute path of "helptab" file with number of help topics."""
        return f"{self.file.absolute()} ({len(self.help_topics)} topics)"


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
        player_level: (int, str, None) = None
        player_class: (list, str) = []
        stats: list = []

        def __init__(self):
            """Initialization of a "help topic" object."""
            self.name = ""
            self.level = 0
            self.aliases = []
            self.body_html = ""
            self.body_text = ""
            self.see_also = []
            self.player_level = None
            self.player_class = []
            self.stats = []

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

        def parse_content_line(self, content_line: str):
            """Parse single line from the content of a help section."""

            # Check whether the line is for a player level.
            if self.player_level is None:
                lvl_match = PLAYER_LEVEL_REGEX.findall(string=content_line)
                if lvl_match and lvl_match[0] and lvl_match[0][1]:
                    player_level = lvl_match[0][1].strip()

                    # If player level is numeric, set integer, otherwise string.
                    if player_level.isnumeric():
                        self.player_level = int(player_level)
                    else:
                        self.player_level = player_level
                    return

            # Check whether the line is for a player class.
            if not self.player_class:
                cls_match = PLAYER_CLASS_REGEX.findall(string=content_line)
                if cls_match and cls_match[0] and cls_match[0][1]:
                    pclass = cls_match[0][1].strip()
                    for splitter in (",", "|", "/"):
                        if splitter in pclass:
                            psplit = pclass.split(splitter)
                            for pcls in psplit:
                                pcls = pcls.strip()
                                if pcls and pcls not in ("", splitter):
                                    if pclass in PLAYER_CLASS_NAMES:
                                        self.player_class.append(pcls)
                            return

                    if not self.player_class:
                        if pclass in PLAYER_CLASS_NAMES:
                            self.player_class.append(pclass)
                    return

            # Check whether the line is for stats.
            if not self.stats:
                stats_match = PLAYER_STATS_REGEX.findall(string=content_line)
                if stats_match and stats_match[0] and stats_match[0][1]:
                    stat_line = stats_match[0][1].strip()
                    for splitter in (",", "|", "/"):
                        if splitter in stat_line:
                            stat_split = stat_line.split(splitter)
                            for stat_item in stat_split:
                                stat_item = stat_item.strip()
                                if stat_item and stat_item != splitter:
                                    logger.debug(f"stats: {self.stats}")
                                    logger.debug(f"type(stats): {type(self.stats)}")
                                    self.stats.append(stat_item)
                            return

                    if not self.stats:
                        self.stats.append(stat_line)
                    return

            # Check if the line is "see also" (related topic) text.
            if not self.see_also:
                see_also_match = SEE_ALSO_REGEX.match(string=content_line)
                if see_also_match:
                    see_also_topics = see_also_match[2].split(",")
                    for see_also_topic in see_also_match[2].split(","):
                        see_also_topic = see_also_topic.strip()
                        if see_also_topic and see_also_topic != "":
                            self.see_also.append(see_also_topic)
                    return

            # Replace HTML tags in body text.
            body_line = content_line
            for (old, new) in ((">", "g"), ("<", "l")):
                body_line = body_line.replace(old, f"&{new}t;")

            for body_item, body_regex in BODY_REGEXES.items():
                body_find = body_regex.findall(string=body_line)
                if body_find and body_find[0]:
                    body_match = body_find[0]
                    self.__setattr__(body_item, body_match[1])
                    return

            self.body_html += f"{body_line}<br>\n"
            self.body_text += f"{body_line}\n"

        def parse_content(self, content: str):
            """Parse the content (below "*") of a "helptab" section."""

            # Iterate each line of the help topic content.
            for content_line in content.split('\n'):
                self.parse_content_line(content_line=content_line)

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
            """Show the object type with name string."""
            return f"<{self.__class__.__name__}> {self.__str__()}"

        def __str__(self) -> str:
            """Show the name of the help topic."""
            return self.name

    def discover(self) -> list:
        """Discover sections within "helptab" file."""
        # Open the "helptab" file (read-only), and gather its entire contents.
        with open(file=self.file, mode="r", encoding="utf-8") as helptab_fh:
            helptab_fo = helptab_fh.read()

        # Sections in "helptab" file are separated by "#" on a line alone.
        return helptab_fo.split(START_STRING)[1].split("\n#\n")

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
                topics[help_topic.name] = help_topic

        # Return complete list of help topics parsed from "helptab" sections.
        return topics
