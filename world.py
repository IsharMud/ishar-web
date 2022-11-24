"""World"""
from flask import Blueprint, flash, render_template
from mud_secret import HELPTAB

def get_help_areas(helptab_file=HELPTAB):
    """
    Method to scrape "areas" from game helptab file
    The "areas" are each listed in the "helptab" file on lines starting with "32 Area "
        followed by descriptions until the character "#" on a single line itself
    """

    # Prepare an empty "areas" dictionary
    #   and do not keep lines by default
    areas = {}
    keep = False

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


world = Blueprint('world', __name__)

@world.route('/areas/<string:area>/', methods=['GET'])
@world.route('/areas/', methods=['GET'])
@world.route('/areas/<string:area>', methods=['GET'])
@world.route('/areas', methods=['GET'])
@world.route('/world/<string:area>/', methods=['GET'])
@world.route('/world/', methods=['GET'])
@world.route('/world/<string:area>', methods=['GET'])
@world.route('/world', methods=['GET'])
def index(area=None):
    """World page that uses the game's existing helptab file
        to display information about each in-game area"""

    # Get all areas from the helptab file, and try to find an area based on any user input
    areas = get_help_areas()
    code = 200

    if area:
        if area in areas.keys():
            areas = areas[area]
        else:
            area = None
            code = 404
            flash('Sorry, but please choose a valid area!', 'error')

    return render_template('world.html.j2', areas=areas, area=area), code
