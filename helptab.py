"""Read/process the "helptab" file used by the MUD itself in-game"""
from mud_secret import HELPTAB


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


def get_helptab(helptab_file=HELPTAB):
    """WIP method to scrape topics from game helptab file"""

    with open(helptab_file, mode='r', encoding='utf8') as helptab_fh:

        topics      = {}
        keep        = False

        for line in helptab_fh:

            stripped    = line.strip()

            if stripped.startswith('32 '):
                topic           = stripped.replace('32 ', '')
                topics[topic]   = str()

            elif stripped == '*':
                keep    = True

            elif stripped == '#':
                keep    = False

            if keep and topics and topic and line:
                topics[topic]   += line

    return topics
