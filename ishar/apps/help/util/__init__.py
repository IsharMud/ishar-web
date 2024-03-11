"""Parse the MUD 'helptab' file."""
import re

from django.conf import settings

from ishar.apps.classes.models import Class


# Compile a few regular expressions for use later
#   to parse out specific items from help topic chunks
pattern = r'^ *(see also|also see|also see help on|see help on|related) *\: *'
see_also_regex = re.compile(pattern=pattern, flags=re.IGNORECASE)
regexes = {
    'syntax': re.compile(r'^ *(Syntax|syntax) *\: *(.+)$'),
    'minimum': re.compile(r'^ *(Minimum|minimum|Min|min) *\: *(.+)$'),
    'level': re.compile(r'^ *(Level|level) *\: *(.+)$'),
    'class': re.compile(r'^ *(Class|Classes) *\: *(.+)$'),
    'component': re.compile(r'^ *(Component|Components) *\: *(.+)$'),
    'save': re.compile(r'^ *(Saves?) *\: *(.+)$'),
    'stats': re.compile(r'^ *(Stats?) *\: *(.+)$'),
    'topic': re.compile(r'^ *(Topic) *\: *(.+)$')
}


def get_help_chunks(help_file=settings.HELPTAB):
    """Parse the MUD 'helptab' file into chunks,
        by '#' character, to roughly separate topics"""

    # Open the 'helptab' file (read-only)
    with open(file=help_file, mode='r', encoding='utf-8') as help_fh:

        # Split the contents of the file into a list,
        #   where each item is separated by "\n#\n":
        #   hash (#) on a line by itself
        #   and return "chunks" except the first (instructions/example)
        return help_fh.read().split('\n#\n')[1:]


def get_help_topics():
    """
    Parse the MUD 'helptab' file chunked list into dictionary of topics.
    """

    # Get helptab file list of chunks
    help_chunks = get_help_chunks()
    help_topics = {}

    # Loop through each chunk from the list
    for help_chunk in help_chunks:

        # Parse the chunk from the list
        parsed_chunk = parse_help_chunk(help_chunk=help_chunk)

        # If the chunk was parsed, and named,
        #   add it to a dictionary of topics to return
        if parsed_chunk and 'name' in parsed_chunk:
            parsed_name = parsed_chunk['name']
            help_topics[parsed_name] = parsed_chunk

    # Return a dictionary of topics, parsed from the list of chunks
    return help_topics


def parse_help_chunk(help_chunk=None):
    """Parse a single chunk from the MUD 'helptab' file into a help topic"""

    # Split the chunk in half on the separator,
    #   between its header and body text:
    #   "\n*\n" - asterisk (*), on a line by itself
    halves = help_chunk.split('\n*\n')
    help_topic = {}

    # Proceed if there are two halves
    if len(halves) == 2:

        # Parse the help topic header, which is everything before '*'
        help_header = parse_help_header(header=halves[0])

        # Proceed if the help header is valid
        if help_header and 'name' in help_header:
            help_content = halves[1]
            help_topic = parse_help_content(content=help_content)
            help_topic['name'] = help_header['name']
            help_topic['aliases'] = help_header['aliases']

    # Return the help topic dictionary
    return help_topic


def parse_help_body(line=None):
    """Parse a single line from a single topic chunk of the MUD 'helptab' file,
        using regular expressions to find specific items
            (such as Class, Syntax, etc.)"""

    # Loop through each item regular expression, looking for matches on items
    line = line.replace('>', '&gt;').replace('<', '&lt;')
    for item_name, regex in regexes.items():
        find = regex.findall(line)
        if find:
            ret = {}
            item_value = find[0][1]

            # Handle class matches with a separate function
            if item_name == 'class':
                item_value = parse_help_class(class_line=item_value)

            # Return the dictionary for any matches
            ret[item_name] = item_value
            return ret

    # Simply return the line that we received, if there was no match
    return line


def parse_help_class(class_line=None):
    """
    Parse a single class line from a single topic chunk
        from the MUD 'helptab' file, and link the Player Class help page.
    """

    topic_classes = class_line.split('/')
    num_topic_classes = len(topic_classes)
    string_out = str()
    i = 0

    playable_classes = Class.objects.filter(
        is_playable=True
    ).values_list("class_name", flat=True)

    for topic_class in topic_classes:
        i += 1
        topic_class = topic_class.strip()
        if topic_class in playable_classes:
            string_out += (
                f'<a href="/help/{topic_class}"'
                f' title="Help: {topic_class} (Class)">'
                f'{topic_class}</a>'
            )
            if i != num_topic_classes:
                string_out += ', '
        else:
            string_out = class_line
    return string_out


def parse_help_content(content=None):
    """Parse the body content from a single topic chunk
        from the MUD 'helptab' file to return a help topic dictionary"""

    # Topic body text is everything after the header and '*',
    #   but replace < and > and " with HTML-safe versions

    # Loop through each line of the help chunk body text
    is_see_also = False
    help_topic = {
        'body_html': str(),
        'body_text': str(),
        'see_also': []
    }
    for line in content.split('\n'):

        # Split up, append, and try to link related topics appropriately
        if see_also_regex.match(line):
            help_topic['body_html'] += 'See Also: '
            help_topic['body_text'] += 'See Also: '
            is_see_also = True

        if is_see_also:
            i = 0
            rm_begin = line.split(':')
            related_topics = rm_begin[-1].strip().split(',')
            num_related = len(related_topics)

            # Loop through each related topic to link them
            for related_topic in related_topics:
                i += 1
                if related_topic and related_topic.strip() != '':
                    related_link = (
                        f'<a href="/help/{related_topic.strip()}"'
                        f' title="Help: {related_topic.strip()}">'
                        f'{related_topic.strip()}</a>'
                    )
                    help_topic['body_html'] += related_link
                    help_topic['body_text'] += related_topic.strip()
                    help_topic['see_also'].append(related_topic.strip())

                    # Comma-separate related help topics
                    if i != num_related:
                        help_topic['body_html'] += ', '
                        help_topic['body_text'] += ', '
                    else:
                        is_see_also = False

        # Parse anything else as if it is the body
        else:
            parsed_line = parse_help_body(line=line)

            # Append strings to the body html and body text, appropriately
            if isinstance(parsed_line, str):
                help_topic['body_html'] += parsed_line + '\n'
                help_topic['body_text'] += line + '\n'

            # Set dictionary values from regex matches
            if isinstance(parsed_line, dict):
                for item_name, item_value in parsed_line.items():
                    help_topic[item_name] = item_value

    # Replace "`help command'" in the body html with link to that help command
    cmd_pattern = r"`help ([\w| ]+)'"
    help_topic['body_html'] = re.sub(
        cmd_pattern,
        r'`<a href="/help/\1" title="Help: \1">help \1</a>`',
        help_topic['body_html'],
        re.MULTILINE
    )

    # Return the help topic
    return help_topic


def parse_help_header(header=None):
    """
    Parse the header of a single topic chunk from the MUD 'helptab' file.
    """

    # The level that the help topic is for, is a number alone,
    #   on the first line of the header
    help_header = {}
    lines = header.split('\n')

    # Name the topic if mortals should reach it, and it starts with "32 "
    if int(lines[0].strip()) < settings.MIN_IMMORTAL_LEVEL and lines[1].startswith('32 '):
        help_header['name'] = lines[1].replace('32 ', '').strip()
        help_header['aliases'] = []

        # Loop through each line of the header
        for header_line in lines:

            # Any lines starting with '32 ' are potential names/aliases
            if header_line.startswith('32 '):

                # Set any aliases, which are not the primary name
                header_line_clean = header_line.replace('32 ', '').strip()
                if header_line_clean != help_header['name']:
                    help_header['aliases'].append(header_line_clean)

    # Return the help topic header
    return help_header


def search_help_topics(all_topics=None, search=None):
    """Search all help topics for a specific topic name or alias"""

    # Get all help topics, if necessary
    if not all_topics:
        all_topics = get_help_topics()

    # If there is no search, return all help topics
    if search is None:
        help_topics = all_topics

    # Loop through each topic to find any matches in the names or aliases
    else:
        help_topics = {}
        search = search.lower()
        for tname, tvals in all_topics.items():

            # Return exact name matches immediately
            if search == tname.lower():
                return {tname: tvals}

            # Add partial name matches
            if search in tname.lower():
                help_topics[tname] = tvals

            # If there was no name match, check aliases
            else:

                # Loop through each alias
                for topic_alias in tvals['aliases']:

                    # Return exact alias matches immediately
                    if search == topic_alias.lower():
                        return {topic_alias: tvals}

                    # Add partial alias matches
                    if search in topic_alias.lower():
                        help_topics[topic_alias] = tvals

    # Return any partial matches
    return help_topics
