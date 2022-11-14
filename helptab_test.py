"""Read/process the "helptab" file used by the MUD"""
import re
from mud_secret import HELPTAB

def get_help(helptab_file=HELPTAB):

    all_help    = None

    with open(file=helptab_file, mode='r', encoding='utf-8') as helptab_fh:
        all_help    = helptab_fh.read()
    helptab_fh.close()

    return all_help

help_topics = get_help().split('\n#\n')
names   = re.compile('[0-9]{0,2} [a-zA-Z]+')
names   = re.compile('[0-9]{0,2} [a-zA-Z]+')

i   = 0
for help_topic in help_topics:

    lines   = help_topic.split('\n')
    line_no = 0
    HEADER  = True
    for line in lines:
        stripped    = line.strip()
        line_no += 1

        print(f'{line_no}: {line}')

        if line == '*':
            HEADER  = False
            continue

        if HEADER:
            if line_no == 1 and stripped.isdigit():
                level   = int(stripped)

            elif names.match(stripped):
                name    = stripped
                print('Name:', name)

        if not HEADER:

            if stripped.startswith('Syntax :'):
                syntax  = stripped
                print('Syntax:', syntax)

            elif stripped.startswith('See also: '):
                similar  = stripped.replace('See also: ', '')
                similars    = similar.split(',')
                print('Similar:', similar)
                print('Similars:', similars)
