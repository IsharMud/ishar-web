"""Read/process the "helptab" file used by the MUD itself in-game"""
import helptab_secret
def get_help_areas(helptab_file=helptab_secret.FILENAME):
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
