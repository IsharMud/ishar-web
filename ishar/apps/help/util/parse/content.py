import re
from .body import parse_help_body


def parse_help_content(content=None):
    """Parse the body content from a single topic chunk
        from the MUD 'helptab' file to return a help topic dictionary"""

    # Topic body text is everything after the header and '*',
    #   but replace < and > and " with HTML-safe versions

    # Loop through each line of the help chunk body text
    is_see_also = False
    help_topic = {
        'body_html': str(),
        'body_text': str(),
        'see_also': []
    }
    for line in content.split('\n'):

        # Split up, append, and try to link related topics appropriately
        if see_also_regex.match(line):
            help_topic['body_html'] += 'See Also: '
            help_topic['body_text'] += 'See Also: '
            is_see_also = True

        if is_see_also:
            i = 0
            rm_begin = line.split(':')
            related_topics = rm_begin[-1].strip().split(',')
            num_related = len(related_topics)

            # Loop through each related topic to link them
            for related_topic in related_topics:
                i += 1
                if related_topic and related_topic.strip() != '':
                    related_link = (
                        f'<a href="/help/{related_topic.strip()}"'
                        f' title="Help: {related_topic.strip()}">'
                        f'{related_topic.strip()}</a>'
                    )
                    help_topic['body_html'] += related_link
                    help_topic['body_text'] += related_topic.strip()
                    help_topic['see_also'].append(related_topic.strip())

                    # Comma-separate related help topics
                    if i != num_related:
                        help_topic['body_html'] += ', '
                        help_topic['body_text'] += ', '
                    else:
                        is_see_also = False

        # Parse anything else as if it is the body
        else:
            parsed_line = parse_help_body(line=line)

            # Append strings to the body html and body text, appropriately
            if isinstance(parsed_line, str):
                help_topic['body_html'] += parsed_line + '\n'
                help_topic['body_text'] += line + '\n'

            # Set dictionary values from regex matches
            if isinstance(parsed_line, dict):
                for item_name, item_value in parsed_line.items():
                    help_topic[item_name] = item_value

    # Replace "`help command'" in the body html with link to that help command
    cmd_pattern = r"`help ([\w| ]+)'"
    help_topic['body_html'] = re.sub(
        cmd_pattern,
        r'`<a href="/help/\1" title="Help: \1">help \1</a>`',
        help_topic['body_html'],
        re.MULTILINE
    )

    # Return the help topic
    return help_topic
