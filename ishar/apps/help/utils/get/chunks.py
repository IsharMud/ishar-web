from django.conf import settings


def get_help_chunks(help_file=settings.HELPTAB):
    """Parse the MUD 'helptab' file into chunks,
        by '#' character, to roughly separate topics"""

    # Open the 'helptab' file (read-only)
    with open(file=help_file, mode='r', encoding='utf-8') as help_fh:

        # Split the contents of the file into a list,
        #   where each item is separated by "\n#\n":
        #   hash (#) on a line by itself
        #   and return "chunks" except the first (instructions/example)
        return help_fh.read().split('\n#\n')[1:]
