"""Help (and World) pages"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.forms import HelpSearchForm
from help.helptab import get_help_topics, search_help_topics


# Flask Blueprint
help_page_bp = Blueprint('help_page', __name__)


@help_page_bp.route('/help/', methods=['GET'])
@help_page_bp.route('/help', methods=['GET'])
def index():
    """Main help page lists help topics"""

    # Redirect form searches to /help/<search>
    if request.args.get('search'):
        return redirect(
            url_for('help.help_page.single', topic=request.args.get('search'))
        )

    return render_template(
        'help_page.html.j2',
        topic=None,
        topics=get_help_topics(),
        help_search_form=HelpSearchForm()
    )


@help_page_bp.route('/help/<string:topic>/', methods=['GET'])
@help_page_bp.route('/help/<string:topic>', methods=['GET'])
def single(topic=None):
    """Display a single help topic, or search results"""

    # Get all topics and the search form
    all_topics = get_help_topics()
    search_form = HelpSearchForm()

    # Return the topic, and its full contents, if there is an exact name match
    if topic in all_topics:
        return render_template(
            'help_page.html.j2',
            topic=all_topics[topic],
            topics=all_topics,
            help_search_form=search_form
        )

    # Try to find matching help topics, and redirect to single match by name
    #   which would then be handled by the render_template above
    search_topics = search_help_topics(all_topics=all_topics, search=topic)
    if len(search_topics) == 1:
        found_topic = next(iter(search_topics.values()))
        return redirect(
            url_for('help.help_page.single', topic=found_topic['name'])
        )

    # Respond with a 200 showing any results,
    # unless there were no results: then, show error with all help topics
    code = 200
    if not search_topics:
        code = 404
        flash('Sorry, but no topics could be found!', 'error')
        search_topics = all_topics

    return render_template(
        'help_page.html.j2',
        topic=None,
        topics=search_topics,
        help_search_form=search_form
    ), code
