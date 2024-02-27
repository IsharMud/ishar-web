
def parse_help_header(header=None):
    """
    Parse the header of a single topic chunk from the MUD 'helptab' file.
    """

    # The level that the help topic is for, is a number alone,
    #   on the first line of the header
    help_header = {}
    lines = header.split('\n')

    # Name the topic if mortals should reach it, and it starts with "32 "
    if int(lines[0].strip()) < settings.MIN_IMMORTAL_LEVEL and lines[1].startswith('32 '):
        help_header['name'] = lines[1].replace('32 ', '').strip()
        help_header['aliases'] = []

        # Loop through each line of the header
        for header_line in lines:

            # Any lines starting with '32 ' are potential names/aliases
            if header_line.startswith('32 '):

                # Set any aliases, which are not the primary name
                header_line_clean = header_line.replace('32 ', '').strip()
                if header_line_clean != help_header['name']:
                    help_header['aliases'].append(header_line_clean)

    # Return the help topic header
    return help_header
