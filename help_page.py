"""Help page"""
from flask import abort, Blueprint, flash, redirect, render_template, url_for
from mud_secret import HELPTAB, IMM_LEVELS


def get_help_chunks(help_file=HELPTAB):
    """Parse the MUD 'helptab' file into chunks, by '#' character, to roughly separate topics"""
    # Open the 'helptab' file (read-only)
    try:
        with open(file=help_file, mode='r', encoding='utf-8') as help_fh:

            # Split the contents of the file into a list,
            #   where each item is separated by "\n#\n" - hash (#) on a line by itself
            #   and return "chunks" except the first (instructions/example)
            return help_fh.read().split('\n#\n')[1:]

    # Catch/return any exception, and close the 'helptab' file
    except Exception as err:
        return err

    finally:
        help_fh.close()


def get_help_topics():
    """Parse the MUD 'helptab' file chunked list into topics"""
    # Get helptab file list of chunks
    help_chunks = get_help_chunks()
    help_topics = {}

    # Loop through each chunk from the list
    for help_chunk in help_chunks:

        # Parse the chunk from the list
        parsed_chunk = parse_help_chunk(help_chunk)

        # If the chunk was parsed, and named,
        #   add it to a dictionary of topics to return
        if parsed_chunk and 'name' in parsed_chunk:
            parsed_name = parsed_chunk['name']
            help_topics[parsed_name] = parsed_chunk

    # Return a dictionary of topics, parsed from the list of chunks
    return help_topics


def parse_help_chunk(help_chunk=None):
    """Parse a single chunk from the MUD 'helptab' file"""

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
            help_topic['body_lines'] = help_topic['body_text'].split('\n')

    # Return the help topic dictionary
    return help_topic


def parse_help_header(header=None):
    """Parse the header from a single topic chunk from the MUD 'helptab' file"""

    # The 'level' of the help topic is a number alone, on the first line of the header
    help_header = {}
    header_lines = header.split('\n')
    help_header['level'] = int(header_lines[0].strip())

    # Name the topic if mortals should be able reach it, and it starts with "32 "
    if help_header['level'] < min(IMM_LEVELS) and header_lines[1].startswith('32 '):
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


help_page = Blueprint('help_page', __name__)


@help_page.route('/help/<string:topic>/', methods=['GET'])
@help_page.route('/help/<string:topic>', methods=['GET'])
def single(topic=None):
    """Display a single help topic"""

    # Get all topics, and display exact topic name matches
    topics = get_help_topics()
    if topic in topics:
        return render_template('help_page.html.j2', topic=topics[topic], topics=topics)

    # Loop through each topics aliases to find a match,
    #   and redirect to the primary name if there is one
    for tvals in topics.values():
        if topic in tvals['aliases']:
            return redirect(url_for('help_page.single', topic=tvals['name']))

    # Otherwise, the topic could not be found
    flash('Sorry, but no topics could be found!', 'error')
    abort(404)


@help_page.route('/help/', methods=['GET', 'POST'])
@help_page.route('/help', methods=['GET', 'POST'])
def index():
    """Main help page lists all help topics"""
    return render_template('help_page.html.j2', topic=None, topics=get_help_topics())


@help_page.route('/areas/', methods=['GET'])
@help_page.route('/areas', methods=['GET'])
@help_page.route('/world/', methods=['GET'])
@help_page.route('/world', methods=['GET'])
def world():
    """World page"""
    # Return only the areas from the helptab file
    return render_template('world.html.j2', areas=None)
