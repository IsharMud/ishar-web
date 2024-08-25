#!/usr/bin/python3
from logging import getLogger
from pathlib import Path
# from re import compile as re_compile


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

HELPTAB_FILE = Path(Path(__file__).parent, "helptab")
MIN_IMMORTAL_LEVEL = 21
START_STRING = ("###########################"
                "---BEGIN HELP FILE---###########################\n")

#name_regex = re_compile(r"^32 (?P<cmd>[0-9a-zA-Z ]+)$")
logger = getLogger(__name__)


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

        def __init__(self):
            """Initialization of a "help topic" object."""
            self.name: str = ""
            self.level: int = 0
            self.aliases: list = []
            self.body: str = ""

        def parse_header(self, header_lines: list):
            """Parse header of a "helptab" section to gather aliases."""
            for header_line in header_lines:
                if header_line.startswith("32 "):
                    self.aliases.append(
                        " ".join(header_line.split(" ")[1:]).strip()
                    )

        def parse_body(self, body: str):
            """Parse body of a "helptab" section."""
            self.body = body

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
            contents = helptab_fh.read()

        # Sections in "helptab" file are separated by "#" on a line alone.
        return contents.split(START_STRING)[1].split("\n#\n")

    def parse(self, sections: list) -> dict:
        """Parse "helptab" sections into dictionary of help topic objects."""
        help_topics = {}

        # Iterate each "helptab" section in the list provided.
        for section in sections:

            # Sections contain a header, and a body, separated by "*".
            try:
                header, body = section.split("\n*\n")

            # Log any skipped "helptab" sections which could not be split.
            except ValueError as val_err:
                logger.error(f"Skipping: {section.__repr__()}")
                logger.exception(val_err)
                continue

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

                    # Use first "32 <Name>" as the name of the help topic.
                    name = " ".join(first_line.split(" ")[1:]).strip()

                    # Create a help topic object using the level and name.
                    help_topic = self.HelpTopic()
                    help_topic.level = topic_level
                    help_topic.name = name

                    # Parse the rest of the help topic header, to get aliases.
                    help_topic.parse_header(header_lines=header_lines[2:])

                    # Parse the body (below "*") within the topic section.
                    help_topic.parse_body(body=body)

            # Append newly created help topic object to list of help topics.
            if help_topic is not None and help_topic.name:
                help_topics[help_topic.name] = help_topic

        # Return complete list of help topics parsed from "helptab" sections.
        return help_topics
