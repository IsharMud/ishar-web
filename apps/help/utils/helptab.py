from logging import getLogger
from pathlib import Path
import re
import threading

from django.conf import settings
from django.urls import reverse
from django.utils.html import format_html

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
    flags=re.IGNORECASE,
)

# Compile regular expression to match sections for another level in content.
DIFF_LEVEL_REGEX = re.compile("^%%\s*(?P<diff_level>[0-9]{1,2})$")

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
    "SUB": r'`<a href="/help/\1\#topic" title="Help: \1">help \1</a>`',
}


def _discover_help(path: Path = settings.HELPTAB) -> list:
    # Discover sections within "helptab" file.

    # Open the "helptab" file (read-only), and gather its entire contents.
    with open(file=path, mode="r", encoding="utf-8") as helptab_fh:
        helptab_fo = helptab_fh.read()

    # Sections in "helptab" file are separated by "#" on a line alone.
    return helptab_fo.split(START_STRING)[1].split("\n#\n")


class HelpTab:
    """Interact with MUD "helptab" file sections representing topics."""

    help_topics: dict = {}
    path: Path = settings.HELPTAB

    def __init__(self, path: (Path, str) = settings.HELPTAB):
        # Discover, and parse, help topics from "helptab" file sections.
        if path and isinstance(path, str):
            path = Path(path)
            self.path = path
        self.help_topics = self.parse(_discover_help(path=self.path))

    def __repr__(self) -> str:
        # Show the object type with absolute path and topic count string.
        return f"{self.__class__.__name__}: {self.__str__()}"

    def __str__(self) -> str:
        # Show absolute path of "helptab" file with number of help topics.
        return f"{self.path.absolute()} ({len(self.help_topics)} topics)"

    class HelpTopic:
        """Help topic from "helptab" file."""

        name: str = ""
        level: int = 0
        aliases: set = {}
        body: str = ""
        see_also: set = {}
        syntax: str = ""
        minimum: str = ""
        player_level: (int, str, None) = None
        player_class: (list, str, None) = None
        position: str = ""
        save: str = ""
        stats: list = []
        components: list = []

        def __init__(self):
            # Initialization of a "help topic" object.

            self.name = ""
            self.level = 0
            self.aliases = set()
            self.body = ""
            self.see_also = set()
            self.syntax = ""
            self.minimum = ""
            self.player_level = None
            self.player_class = None
            self.position = ""
            self.save = ""
            self.stats = []
            self.components = []

        @property
        def display_name(self, replace_me: str = "") -> str:
            if self.is_area:
                replace_me = "Area"
            if self.is_spell:
                replace_me = "Spell"
            return self.name.replace(f"{replace_me} ", "")

        def get_absolute_url(self):
            # URL to help topic page, with anchor.
            return reverse(viewname="help_page", args=(self.name,)) + "#topic"

        def parse_header(self, header_lines: list):
            # Parse header of a "helptab" section, to gather aliases.
            for header_line in header_lines:
                if header_line.startswith("32 "):
                    self.aliases.add(" ".join(header_line.split(" ")[1:]).strip())

        def parse_content_line(self, content_line: str):
            # Parse single line from the content of a help section.

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

            # Check whether the line is for position ("Posn"), parsing if so.
            if not self.position and content_line.startswith("Posn   : "):
                self.position = content_line.split(":")[1].strip()
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
                if component_match:
                    self.components = component_match.group("component").split(", ")
                return False

            # Finally, consider the line body text.
            return True

        def parse_content(self, content: str):
            # Parse the content (below "*") of a "helptab" section.

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
            # Boolean whether the help topic is an "Area ".
            if self.name.startswith("Area "):
                return True
            return False

        @property
        def is_spell(self) -> bool:
            # Boolean whether the help topic is a "Spell ".
            if self.name.startswith("Spell "):
                return True
            return False

        @property
        def body_html(self) -> str:
            # Return body text with links, formatted for HTML display.

            # Replace HTML tags in body text.
            body = self.body
            for old, new in ((">", "g"), ("<", "l")):
                body = body.replace(old, f"&{new}t;")

            # Hyperlink "`help command'" in text within body text.
            body = re.sub(
                pattern=HELP_CMD_REGEX["PATTERN"],
                repl=HELP_CMD_REGEX["SUB"],
                string=body,
                flags=re.MULTILINE,
            )
            return body

        @property
        def player_class_html(self) -> str:
            # Parse player class items for web display.

            # If a list, parse each item as a player class to be linked to.
            if isinstance(self.player_class, list):
                class_links = []

                # Hyperlink each player class help page.
                for class_item in self.player_class:
                    link = reverse(
                        viewname="help_page",
                        args=(class_item,)
                    ) + "#topic"
                    link_text = format_html(
                        '<a href="{}">{}</a>',
                        link, class_item
                    )
                    class_links.append(link_text)

                # Return hyperlinks to class help pages.
                return ", ".join(class_links)

            # Return non-list directly.
            return self.player_class

        def alias_count(self) -> int:
            # Count of number of help topic aliases.
            return len(self.aliases)

        def pluralize(self, item="alias"):
            # Pluralize "alias", depending upon count of alias(es).
            if self.alias_count() == 1:
                return item
            return f"{item}es"

        def __repr__(self) -> str:
            # Show object type with name string.
            return f"{self.__class__.__name__}: {self.__str__()}"

        def __str__(self) -> str:
            # Show name of the help topic.
            return self.name

        def __gt__(self, other):
            return self.name > other.name

        def __lt__(self, other):
            return self.name < other.name

    def parse(self, sections: list) -> dict[str:HelpTopic,]:
        # Parse "helptab" sections into dictionary of help topic objects.
        topics = {}

        # Parse report: silently-dropped topics are a recurring "why is X
        # missing?" source (see #51/#84), so tally every skip reason and log a
        # one-line summary — a topic that never shows up is now diagnosable.
        counts = {
            "sections": 0, "kept": 0, "unsplittable": 0,
            "immortal": 0, "not_playing": 0, "headerless": 0,
        }
        dropped_playing = []  # (level, first header line) for non-"32 " drops

        # Iterate each "helptab" section in the list provided.
        for section in sections:

            # Ignore blank trailing chunks left by the section split.
            if not section.strip():
                continue
            counts["sections"] += 1

            # Sections contain a header, and a body, separated by "*".
            try:
                header, content = section.split("\n*\n")

            # Log any skipped "helptab" sections which could not be split.
            except ValueError as val_err:
                counts["unsplittable"] += 1
                logger.error(f"Skipping unsplittable section: {section.__repr__()}")
                logger.exception(val_err)
                continue  # Next section.

            # Start with fresh topic to possibly add to returned list later.
            finally:
                help_topic = None

            # First header line is the player level the section applies to.
            header_lines = header.split("\n")
            try:
                topic_level = int(header_lines[0])
            except (ValueError, IndexError):
                counts["headerless"] += 1
                logger.error(f"Skipping section with no level: {header.__repr__()}")
                continue

            # Only consider helptab sections that are meant for mortal players.
            if topic_level >= settings.MIN_IMMORTAL_LEVEL:
                counts["immortal"] += 1
                continue

            # Only consider helptab sections for "32 " ("Playing") state.
            first_line = header_lines[1].strip() if len(header_lines) > 1 else ""
            if not first_line.startswith("32 "):
                counts["not_playing"] += 1
                if first_line:
                    dropped_playing.append((topic_level, first_line))
                continue

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
            if help_topic.name:
                topics[help_topic.name] = help_topic
                counts["kept"] += 1

        # Emit the parse report so silently-dropped topics are diagnosable.
        logger.info(
            "helptab parse: %d topics kept from %d sections "
            "(%d immortal, %d non-playing, %d unsplittable, %d headerless)",
            counts["kept"], counts["sections"], counts["immortal"],
            counts["not_playing"], counts["unsplittable"], counts["headerless"],
        )
        if dropped_playing:
            logger.debug(
                "helptab non-playing drops (level, first line): %s",
                "; ".join(f"[{lvl}] {line}" for lvl, line in dropped_playing[:50]),
            )

        # Return complete list of help topics parsed from "helptab" sections.
        return topics

    def search(self, search_name: str) -> dict[str:HelpTopic,]:
        # Search help topic names and aliases via a deterministic ladder.
        #
        # The old search was a single substring sweep over every name and
        # alias, so "heal" dragged in "Score" (whose "Health" alias contains
        # "heal") and results had no relevance order. Instead, sort every
        # topic into the *best* tier it matches and return the first non-empty
        # tier, so a cleaner match always wins over a looser one. Name matches
        # rank above alias matches, then exact > prefix > substring within each:
        #
        #   1. exact topic name      (case-insensitive)
        #   2. exact alias           (case-insensitive)
        #   3. topic-name prefix
        #   4. topic-name substring
        #   5. alias prefix
        #   6. alias substring
        #
        # Name-before-alias is what fully fixes "heal" -> "Score": "Health" is
        # a *prefix* of "heal", so a name/alias-blind ladder still surfaces
        # Score at the alias tier; ranking name-substring (4) above alias-prefix
        # (5) returns the actual "Spell Heal*" topics and drops Score entirely.
        # Verified against the live helptab (see the PR / decisions.md).
        query = (search_name or "").strip()
        if not query:
            return {}
        q = query.casefold()

        tiers = ({}, {}, {}, {}, {}, {})
        exact_name, exact_alias, name_pfx, name_sub, alias_pfx, alias_sub = tiers
        for topic_name, topic in self.help_topics.items():
            name_cf = topic_name.casefold()
            aliases_cf = [alias.casefold() for alias in topic.aliases]

            if name_cf == q:
                exact_name[topic_name] = topic
            elif q in aliases_cf:
                exact_alias[topic_name] = topic
            elif name_cf.startswith(q):
                name_pfx[topic_name] = topic
            elif q in name_cf:
                name_sub[topic_name] = topic
            elif any(alias.startswith(q) for alias in aliases_cf):
                alias_pfx[topic_name] = topic
            elif any(q in alias for alias in aliases_cf):
                alias_sub[topic_name] = topic

        # Return the strongest non-empty tier, name-sorted for stable output.
        for tier in tiers:
            if tier:
                return dict(sorted(tier.items()))
        return {}

    def suggest(self, search_name: str, limit: int = 6) -> list[str]:
        # "Did you mean" fallback for a 404: closest topic names/aliases.
        #
        # difflib (stdlib) gives fuzzy suggestions for typos the prefix/
        # substring tiers miss ("metero" -> "Meteor Swarm"), with no new
        # dependency. Match against names *and* aliases but only ever suggest
        # canonical topic names.
        from difflib import get_close_matches

        query = (search_name or "").strip().casefold()
        if not query:
            return []

        # Map every searchable handle (name or alias, folded) to its topic.
        handles: dict[str, str] = {}
        for topic_name, topic in self.help_topics.items():
            handles.setdefault(topic_name.casefold(), topic_name)
            for alias in topic.aliases:
                handles.setdefault(alias.casefold(), topic_name)

        # Ordered, de-duplicated topic names from the closest handles.
        suggestions: list[str] = []
        for handle in get_close_matches(query, handles.keys(), n=limit * 2, cutoff=0.6):
            topic_name = handles[handle]
            if topic_name not in suggestions:
                suggestions.append(topic_name)
            if len(suggestions) >= limit:
                break
        return suggestions


# Module-level cache so the helptab is parsed once and re-parsed only when the
# file changes. The file is a live mount from the game, so the old
# ``HELPTAB = HelpTab()`` at import pinned the parse to Daphne start — helptab
# edits only appeared after the next web deploy. Now each request re-stats the
# file and re-parses on mtime change, keeping the last good parse if a re-parse
# ever fails (a bad edit degrades to stale, never to a 500).
_helptab_lock = threading.Lock()
_helptab_cache = {"helptab": None, "mtime": None, "path": None}


def get_helptab(path: (Path, str) = None) -> HelpTab:
    """Return a cached HelpTab, re-parsing when the file's mtime changes."""
    if path is None:
        path = settings.HELPTAB
    path = Path(path)

    # Stat the file; if it's momentarily unreadable (e.g. mid-deploy remount),
    # serve the last good parse rather than erroring.
    try:
        mtime = path.stat().st_mtime
    except OSError as os_err:
        with _helptab_lock:
            if _helptab_cache["helptab"] is not None:
                logger.error("Could not stat helptab %s: %s", path, os_err)
                return _helptab_cache["helptab"]
        raise

    with _helptab_lock:
        cached = _helptab_cache["helptab"]
        if (
            cached is not None
            and _helptab_cache["mtime"] == mtime
            and _helptab_cache["path"] == path
        ):
            return cached

        # Parse under the lock so a burst of concurrent requests doesn't each
        # re-parse the same ~550KB file; the parse is fast and help traffic is
        # light, so serializing is cheaper than a thundering herd.
        try:
            parsed = HelpTab(path=path)
        except Exception:
            if cached is not None:
                logger.exception(
                    "Re-parsing helptab %s failed; serving last good parse", path
                )
                return cached
            raise

        _helptab_cache.update(helptab=parsed, mtime=mtime, path=path)
        return parsed
