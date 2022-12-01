"""Help page"""
import re
from flask import Blueprint, flash, render_template
from mud_secret import HELPTAB, IMM_LEVELS

def get_all_help(helptab_file=HELPTAB):
    """Read/process the 'helptab' file used by the MUD"""
    all_help = None

    with open(file=helptab_file, mode='r', encoding='utf-8') as helptab_fh:
        all_help = helptab_fh.read()
    helptab_fh.close()

    return all_help


def get_helptab(areas=False, topic=None):
    """Find help in helptab"""

    help_topics = get_all_help().split('\n#\n')
    topics = {}
    names = re.compile(r'32 [a-zA-Z]+')
    if areas:
        names = re.compile(r'32 Area [a-zA-Z]+')

    for help_topic in help_topics:

        lines = help_topic.split('\n')
        line_no = 0
        in_header = True
        in_related = False

        this_topic = {
            'level':    int(),
            'aliases':  [],
            'text':     '',
            'see_also': []
        }

        for line in lines:

            stripped = line.strip()
            line_no += 1

            # End of the header
            if stripped == '*':
                in_header = False
                continue

            if stripped.startswith('%% ') or stripped == '#':
                in_related = False
                break

            if in_header:

                if line_no == 1 and stripped.isdigit():
                    this_topic['level'] = int(stripped)

                elif names.match(line):
                    this_topic['aliases'].append(stripped)

            elif not in_header:

                if in_related or stripped.lower().startswith('see also: '):
                    in_related = True
                    see_also = stripped.lower().replace('see also: ', '')
                    see_also = see_also.split(',')
                    for also in see_also:
                        see_topic = also.strip()
                        if see_topic:
                            this_topic['see_also'].append(see_topic)

                elif line.lower().startswith('syntax : '):
                    syntax = stripped.lower().replace('syntax : ', '')
                    this_topic['syntax'] = syntax

                elif line.lower().startswith('minimum: '):
                    minimum = stripped.lower().replace('minimum: ', '')
                    this_topic['minimum'] = minimum

                elif line.lower().startswith('class  : '):
                    player_class = stripped.lower().replace('class  : ', '')
                    this_topic['player_class'] = player_class

                elif line.lower().startswith('level  : '):
                    player_level = stripped.lower().replace('level  : ', '')
                    this_topic['player_level'] = player_level

                elif line.lower().startswith('save   : '):
                    save = stripped.lower().replace('save   : ', '')
                    this_topic['save'] = save

                else:
                    this_topic['text'] += line + "\n"

        if this_topic['aliases'] and this_topic['level'] < min(IMM_LEVELS):
            topic_name = this_topic['aliases'][0].replace('32 ', '').lower()
            topics[topic_name] = this_topic

    return topics


help_page = Blueprint('help_page', __name__)


@help_page.route('/help/<string:topic>', methods=['GET'])
@help_page.route('/help/<string:topic>/', methods=['GET'])
@help_page.route('/help/', methods=['GET'])
@help_page.route('/help', methods=['GET'])
def index(topic=None):
    """Help page that uses the game's existing helptab file
        to display information about each topic"""

    # Get all topics from the helptab file
    topics = get_helptab()
    code = 200

    # Try to find a topic based on any user input
    if topic:
        if topic in topics:
            topic = topics[topic]
        else:
            for jawn in topics:
                print(jawn)

            topic = None
            code = 404

    return render_template('help_page.html.j2', topic=topic, topics=topics), code


@help_page.route('/areas/', methods=['GET'])
@help_page.route('/areas', methods=['GET'])
@help_page.route('/world/', methods=['GET'])
@help_page.route('/world', methods=['GET'])
def world():
    """World page"""
    return render_template('world.html.j2', areas=get_helptab(areas=True))
