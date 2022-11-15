"""helptab"""
import logging
import re
from mud_secret import HELPTAB

# Logging configuration
logging.basicConfig(
    level   = logging.INFO,
    format  = '%(asctime)s [%(levelname)s] %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S %Z'
)

def get_help_areas(helptab_file=HELPTAB):
    """
    Method to scrape "areas" from game helptab file
    The "areas" are each listed in the "helptab" file on lines starting with "32 Area "
        followed by descriptions until the character "#" on a single line itself
    """

    # Prepare an empty "areas" dictionary
    #   and do not keep lines by default
    areas   = {}
    keep    = False

    # Read game "helptab" file
    with open(helptab_file, mode='r', encoding='utf8') as helptab_fh:

        # Loop through each line, finding and keeping chunks staring with "32 Area "
        for line in helptab_fh:
            stripped = line.strip()

            # Stop line (#)
            if keep and stripped == '#':
                keep = False

            # Do not include "other levels" info (%%)
            if keep and stripped.startswith('%% '):
                keep = False

            # Append the current chunk to our areas dictionary,
            #   under the key of whatever started with "32 Area " last
            if keep and not stripped.startswith('32 Area '):
                areas[area_name] += line

            # Start new dictionary keys of chunks at lines beginning with "32 Area "
            if stripped.startswith('32 Area '):
                keep = True
                area_name = stripped.replace('32 Area ', '')
                areas[area_name] = ''

    return areas


def get_all_help(helptab_file=HELPTAB):
    """Read/process the 'helptab' file used by the MUD"""

    all_help    = None

    with open(file=helptab_file, mode='r', encoding='utf-8') as helptab_fh:
        all_help    = helptab_fh.read()
    helptab_fh.close()

    return all_help


def get_helptab():
    """Find help in helptab"""

    help_topics = get_all_help().split('\n#\n')
    topics  = {}
#    names   = re.compile(r'[0-9]{0,2} [a-zA-Z]+')
    names   = re.compile(r'32 [a-zA-Z]+')

    logging.info('Help Topics\t%i', len(help_topics))
    for help_topic in help_topics:

        logging.info('Help Topic:\t%s', help_topic)

        lines   = help_topic.split('\n')
        LINE_NO = 0
        HEADER  = True

        this_topic = {
            'level':    int(),
            'aliases':  [],
            'text':     ''
        }

        for line in lines:

            stripped    = line.strip()
            LINE_NO     += 1

            print(f'{LINE_NO}: {line}')

            # End of the header
            if line == '*':
                HEADER  = False
                continue

            elif stripped.startswith('%% '):
                break

            if HEADER:

                if LINE_NO == 1 and stripped.isdigit():
                    this_topic['level']    = int(stripped)

                elif names.match(line):
                    this_topic['aliases'].append(stripped)

            elif not HEADER:

                if line.startswith('Syntax : '):
                    syntax  = stripped.replace('Syntax : ', '')
                    this_topic['syntax']   = syntax

                elif line.startswith('Minimum: '):
                    minimum = stripped.replace('Minimum: ', '')
                    this_topic['minimum']   = minimum

                elif line.startswith('Class  : '):
                    player_class    = stripped.replace('Class  : ', '')
                    this_topic['player_class']  = player_class

                elif line.startswith('Level  : '):
                    player_level    = stripped.replace('Level  : ', '')
                    this_topic['player_level']  = player_level

                elif line.startswith('Save   : '):
                    save    = stripped.replace('Save   : ', '')
                    this_topic['save']  = save

                elif stripped.startswith('See also: '):
                    similar  = stripped.replace('See also: ', '')
                    this_topic['related']  = similar.split(',')

                else:
                    this_topic['text'] += line + "\n"

        print(this_topic)
        if this_topic['aliases'] and this_topic['level'] < 20:
            topic_name  = this_topic['aliases'][0].replace('32 ', '')
            topics[topic_name]  = this_topic

    return topics
