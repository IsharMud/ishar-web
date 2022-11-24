"""Help page"""
import re
from flask import Blueprint, flash, render_template
from mud_secret import HELPTAB

def get_all_help(helptab_file=HELPTAB):
    """Read/process the 'helptab' file used by the MUD"""
    all_help = None

    with open(file=helptab_file, mode='r', encoding='utf-8') as helptab_fh:
        all_help = helptab_fh.read()
    helptab_fh.close()

    return all_help


def get_helptab():
    """Find help in helptab"""

    help_topics = get_all_help().split('\n#\n')
    topics = {}
#    names = re.compile(r'[0-9]{0,2} [a-zA-Z]+')
    names = re.compile(r'32 [a-zA-Z]+')

    for help_topic in help_topics:

        lines = help_topic.split('\n')
        line_no = 0
        in_header = True

        this_topic = {
            'level':    int(),
            'aliases':  [],
            'text':     ''
        }

        for line in lines:

            stripped = line.strip()
            line_no += 1

            # End of the header
            if line == '*':
                in_header = False
                continue

            if stripped.startswith('%% '):
                break

            if in_header:

                if line_no == 1 and stripped.isdigit():
                    this_topic['level'] = int(stripped)

                elif names.match(line):
                    this_topic['aliases'].append(stripped)

            elif not in_header:

                if line.startswith('Syntax : '):
                    syntax = stripped.replace('Syntax : ', '')
                    this_topic['syntax'] = syntax

                elif line.startswith('Minimum: '):
                    minimum = stripped.replace('Minimum: ', '')
                    this_topic['minimum'] = minimum

                elif line.startswith('Class  : '):
                    player_class = stripped.replace('Class  : ', '')
                    this_topic['player_class'] = player_class

                elif line.startswith('Level  : '):
                    player_level = stripped.replace('Level  : ', '')
                    this_topic['player_level'] = player_level

                elif line.startswith('Save   : '):
                    save = stripped.replace('Save   : ', '')
                    this_topic['save'] = save

                elif stripped.startswith('See also: '):
                    similar = stripped.replace('See also: ', '')
                    this_topic['related'] = similar.split(',')

                else:
                    this_topic['text'] += line + "\n"

        if this_topic['aliases'] and this_topic['level'] < 20:
            topic_name = this_topic['aliases'][0].replace('32 ', '')
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
        if topic in topics.keys():
            topic = topics[topic]
        else:
            topic = None
            code = 404
            flash('Sorry, but please choose a valid topic!', 'error')

    return render_template('help_page.html.j2', topic=topic, topics=topics), code
