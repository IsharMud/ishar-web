import re

from .pclass import parse_help_class


def parse_help_body(line=None):
    """Parse a single line from a single topic chunk of the MUD 'helptab' file,
        using regular expressions to find specific items
            (such as Class, Syntax, etc.)"""

    # Compile regular expressions to parse items from help topic chunks.
    regexes = {
        'syntax': re.compile(r'^ *(Syntax|syntax) *\: *(.+)$'),
        'minimum': re.compile(r'^ *(Minimum|minimum|Min|min) *\: *(.+)$'),
        'level': re.compile(r'^ *(Level|level) *\: *(.+)$'),
        'class': re.compile(r'^ *(Class|Classes) *\: *(.+)$'),
        'component': re.compile(r'^ *(Component|Components) *\: *(.+)$'),
        'save': re.compile(r'^ *(Saves?) *\: *(.+)$'),
        'stats': re.compile(r'^ *(Stats?) *\: *(.+)$'),
        'topic': re.compile(r'^ *(Topic) *\: *(.+)$')
    }

    # Loop through each item regular expression, looking for matches on items
    line = line.replace('>', '&gt;').replace('<', '&lt;')
    for item_name, regex in regexes.items():
        find = regex.findall(line)
        if find:
            ret = {}
            item_value = find[0][1]

            # Handle class matches with a separate function
            if item_name == 'class':
                item_value = parse_help_class(class_line=item_value)

            # Return the dictionary for any matches
            ret[item_name] = item_value
            return ret

    # Simply return the line that we received, if there was no match
    return line
