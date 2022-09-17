"""Read/process the "helptab" file used by the MUD itself in-game"""
import helptab_secret
with open(helptab_secret.FILENAME, mode='r', encoding='utf8') as helptab_fh:
    diff_count = total_count = 0
    for line in helptab_fh:
        stripped    = line.strip()
        if stripped.startswith('32 '):
            print('Start: ', stripped)
        if stripped == '#':
            print('End: ', stripped)
