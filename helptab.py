"""Parse the MUD 'helptab' file"""
import re
from mud_secret import HELPTAB, IMM_LEVELS
from sentry import sentry_sdk


def get_help_chunks(help_file=HELPTAB):
    """Parse the MUD 'helptab' file into chunks, by '#' character, to roughly separate topics"""

    # Open the 'helptab' file (read-only)
    try:
        with open(file=help_file, mode='r', encoding='utf-8') as help_fh:

            # Split the contents of the file into a list,
            #   where each item is separated by "\n#\n" - hash (#) on a line by itself
            #   and return "chunks" except the first (instructions/example)
            return help_fh.read().split('\n#\n')[1:]

    # Catch/return exceptions or errors on accessing the 'helptab' file,
    #   and report to Sentry
    except (FileNotFoundError, PermissionError, Exception) as err:
        sentry_sdk.capture_exception(err)
        return []

    # Close the 'helptab' file
    finally:
        help_fh.close()


def get_help_topics():
    """Parse the MUD 'helptab' file chunked list into dictionry of topics"""

    # Get helptab file list of chunks
    help_chunks = get_help_chunks()
    help_topics = {}

    # Loop through each chunk from the list
    for help_chunk in help_chunks:

        # Parse the chunk from the list
        parsed_chunk = parse_help_chunk(help_chunk)

        # If the chunk was parsed, and named, add it to a dictionary of topics to return
        if parsed_chunk and 'name' in parsed_chunk:
            parsed_name = parsed_chunk['name']
            help_topics[parsed_name] = parsed_chunk

    # Return a dictionary of topics, parsed from the list of chunks
    return help_topics


def parse_help_chunk(help_chunk=None):
    """Parse a single chunk from the MUD 'helptab' file into a help topic"""

    # Split the chunk in half on the separator, between its header and body text:
    #   "\n*\n" - asterisk (*), on a line by itself
    halves = help_chunk.split('\n*\n')
    help_topic = {}

    # Proceed if there are two halves
    if len(halves) == 2:

        # Parse the help topic header, which is everything before '*'
        help_header = parse_help_header(header=halves[0])

        # Proceed if mortals should be able to reach the topic,
        #   and it starts with "32 "
        if help_header and 'name' in help_header:
            help_topic['name'] = help_header['name']
            help_topic['aliases'] = help_header['aliases']

            # Topic body text is everything after the header and '*'
            help_topic['body_text'] = halves[1].replace('>', '&gt;').replace('<', '&lt;').replace('"', '&quot;')
            for i in ['syntax', 'level', 'minimum', 'class', 'topic', 'save']:
                help_topic[i] = parse_help_body(help_topic['body_text'], i)
            help_topic['see_also'] = parse_help_see_also(help_topic['body_text'])

    # Return the help topic dictionary
    return help_topic


def parse_help_header(header=None):
    """Parse the header from a single topic chunk from the MUD 'helptab' file"""

    # The 'for_level' of the help topic is a number alone, on the first line of the header
    help_header = {}
    header_lines = header.split('\n')
    help_header['for_level'] = int(header_lines[0].strip())

    # Name the topic if mortals should be able reach it, and it starts with "32 "
    if help_header['for_level'] < min(IMM_LEVELS) and header_lines[1].startswith('32 '):
        help_header['name'] = header_lines[1].replace('32 ', '').strip()
        help_header['aliases'] = []

        # Loop through each line of the header
        for header_line in header_lines:

            # Any lines starting with '32 ' are potential names/aliases
            if header_line.startswith('32 '):

                # Set any aliases, which are not the primary name
                header_line_clean = header_line.replace('32 ', '').strip()
                if header_line_clean != help_header['name']:
                    help_header['aliases'].append(header_line_clean)

    # Return the help topic header
    return help_header


def parse_help_body(body=None, search=None):
    """Parse the body from a single topic chunk from the MUD 'helptab' file"""

    # Split the body into lines and loop through each line
    lines = body.split('\n')
    for line in lines:

        # Get the value after the colon (:) for any lines that matched the search
        if re.search(r'^(\s*)(' + search + r')(\s*):(\s*)', line.strip().lower()):
            value = line.split(':')
            return value[-1].strip()

    # No matches returns None
    return None


def parse_help_see_also(body=None):
    """Parse the body from a single topic chunk from the MUD 'helptab' file,
        looking for related topics"""

    # Start an empty list of related help topics,
    #   split the body into lines, and keep no lines by default
    see_also = []
    lines = body.split('\n')
    keep = False

    # Loop through each line of the topic chunk body
    for line in lines:

        # Keep anything after a phrase that seems like it indicates related topics:
        #   such as "see also", "also see", "also see help on", "related" etc.
        if re.search(r'^(\s*)(see also|also see|also see help on|related)(\s*):(\s*)', line.strip().lower()):
            keep = True

        if keep:
            # Remove anything before the colon (:) and get each topic
            rmbegin = line.split(':')
            related_topics = rmbegin[-1].strip().split(',')

            # Append each related topic to our list to return
            for related_topic in related_topics:
                if related_topic and related_topic.strip() != '':
                    see_also.append(related_topic.strip())

        # This only really works because "See also" is always the end of every help topic chunk...
        # If the "See also:" stuff was in the middle of the help topic chunk, keep would remain True...

    # Return the list of related topics
    return see_also


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
                return { tname: tvals }

            # Add partial name matches
            if search in tname.lower():
                help_topics[tname] = tvals

            # If there was no name match, check aliases
            else:

                # Loop through each alias
                for topic_alias in tvals['aliases']:

                    # Return exact alias matches immediately
                    if search == topic_alias.lower():
                        return { topic_alias: tvals }

                    # Add partial alias matches
                    if search in topic_alias.lower():
                        help_topics[topic_alias] = tvals

    # Return any partial matches
    return help_topics
