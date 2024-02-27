from .content import parse_help_content
from .header import parse_help_header


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
