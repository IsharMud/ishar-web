from .chunks import get_help_chunks
from ..parse.chunk import parse_help_chunk


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
