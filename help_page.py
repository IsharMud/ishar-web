"""Help page"""
import re
from flask import Blueprint, flash, redirect, render_template, url_for
from forms import HelpSearchForm
from mud_secret import HELPTAB, IMM_LEVELS


def get_all_help(helptab_file=HELPTAB):
    """Read/process the 'helptab' file used by the MUD"""
    all_help = None

    with open(file=helptab_file, mode='r', encoding='utf-8') as helptab_fh:
        all_help = helptab_fh.read()
    helptab_fh.close()

    return all_help


def get_helptab(regex=re.compile(r'32 [a-zA-Z]+')):
    """Find help in helptab"""

    help_topics = get_all_help().split('\n#\n')
    topics = {}

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

                elif regex.match(line):
                    this_topic['aliases'].append(stripped.lower().replace('32 ', ''))

            elif not in_header:

                if in_related or stripped.lower().startswith('see also: '):
                    in_related = True
                    see_also = stripped.lower().replace('see also: ', '')
                    see_also = see_also.split(',')
                    for also in see_also:
                        see_topic = also.replace('.', '').strip()
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


@help_page.route('/help/', methods=['GET', 'POST'])
@help_page.route('/help', methods=['GET', 'POST'])
def index():
    """Main help page"""

    # Get all topics from the helptab file
    code = 200
    topic = None
    topics = get_helptab()

    # Get help search form and check if submitted
    help_search_form = HelpSearchForm()
    if help_search_form.validate_on_submit():

        # Lower-case the search string
        search_string = help_search_form.help_search_name.data.lower()

        # Use direct match on a topic name
        if search_string in topics:
            return redirect(url_for('help_page.single', topic=search_string))

        # Loop through all available topics...
        for tvals in topics.values():

            # Use direct match on topic alias
            if tvals['aliases'] and search_string in tvals['aliases']:
                return redirect(url_for('help_page.single', topic=tvals['aliases'][0]))

            # Loop through each topics aliases...
            for topic_alias in tvals['aliases']:

                # Use the first alias which starts with, contains, or ends with, the search string
                if topic_alias.startswith(search_string) or search_string in topic_alias or topic_alias.endswith(search_string):
                    return redirect(url_for('help_page.single', topic=tvals['aliases'][0]))

        # If the search made it this far, nothing was found...
        code = 404
        flash('Sorry, but no topics were found!', 'error')

    return render_template('help_page.html.j2', topic=topic, topics=topics,
                            help_search_form=help_search_form
                          ), code


@help_page.route('/help/<string:topic>', methods=['GET'])
@help_page.route('/help/<string:topic>/', methods=['GET'])
def single(topic=None):
    """Help topic page"""

    topics = get_helptab()
    code = 404
    for tvals in topics.values():
        if tvals['aliases'] and topic in tvals['aliases']:
            ret = tvals
            code = 200

    if code == 404:
        ret = None
        flash('Sorry, but that topic was not found!', 'error')

    return render_template('help_page.html.j2', topic=ret, topics=topics, help_search_form=HelpSearchForm()), code


@help_page.route('/areas/', methods=['GET'])
@help_page.route('/areas', methods=['GET'])
@help_page.route('/world/', methods=['GET'])
@help_page.route('/world', methods=['GET'])
def world():
    """World page"""
    # Return only the areas from the helptab file
    return render_template('world.html.j2', areas=get_helptab(regex=re.compile(r'32 Area [a-zA-Z]+')))
