from .pclass import parse_help_class


def parse_help_body(line=None):
    """Parse a single line from a single topic chunk of the MUD 'helptab' file,
        using regular expressions to find specific items
            (such as Class, Syntax, etc.)"""

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
