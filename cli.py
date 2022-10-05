#!/usr/bin/env python3
"""Manage Ishar MUD via CLI with argument parsing"""
from datetime import datetime
from dateutil.relativedelta import relativedelta
import getopt
import os
import sys
import sentry_sdk
from database import db_session
from mud_secret import PODIR
import models

sentry_sdk.init(traces_sample_rate=1.0)

print('Ishar MUD CLI\n')
now = datetime.utcnow()

def finish(code=1, message='Exiting...'):
    """Function to exit with a specific exit code while cleanly closing the database"""
    db_session.close()
    if code != 0:
        sys.stderr.write(f'{message}')
    else:
        print(message)
    sys.exit(code)

def usage():
    """Print usage/help information (-h, --help)"""
    print(f"""Usage: {os.path.basename(__file__)}

    -h  --help              This help information
    -l  --list              List any active season(s)
    --list-all              List any season(s), including inactive seasons
    -c  --create <months>   Create a new active season, of <months> in length
    -e  --expire <ID>       Expire an active season, by its ID

    --pwipe                 Perform a calculation of essence, and confirm before deleting mortals
""")

if __name__ == "__main__":

    try:
        available_opts = {
            'short' : 'hlc:e:',
            'long'  : ['help', 'usage', 'list', 'list-all', 'create=', 'expire=', 'pwipe']
        }
        opts, args = getopt.getopt(sys.argv[1:], available_opts['short'], available_opts['long'])
    except getopt.GetoptError as err:
        usage()
        finish(code=1, message=err)

    for opt, arg in opts:

        # Help / usage info
        if opt in ('-h', '--help', '--usage'):
            usage()
            finish(code=0, message='')

        # Create
        elif opt in ('--create'):
            try:
                expire  = now + relativedelta(months=int(arg))
                season  = models.Season(
                    is_active       = 1,
                    effective_date  = now,
                    expiration_date = expire
                )
            except Exception as err:
                finish(code=1, message=f'Invalid new season creation\n{err}')

            if season:
                print(season)
                do_create = input('Create? y/[n] ')
                if do_create.lower() == 'y' or do_create.lower() == 'yes':
                    db_session.add(season)
                    db_session.commit()
                    print('Created:', season.season_id)
                    finish(code=0, message=season)

        # Expiration
        elif opt in ('-e', '-x', '--expire'):
            season = models.Season.query.filter_by(
                        season_id   = int(arg),
                    ).first()
            if season:
                print(season)
                do_expire = input('Expire? y/[n] ')
                if do_expire.lower() == 'y' or do_expire.lower() == 'yes':
                    season.is_active        = 0
                    season.expiration_date  = now
                    db_session.commit()
                    print('Expired:\n')
                    finish(
                        code    = 0,
                        message = models.Season.query.filter_by(season_id=int(arg)).first()
                    )
            else:
                finish(code=1, message='Invalid season expiration')

        # Player wipe
        elif opt == '--pwipe':
            podir_del   = []
            for account in models.Account.query.filter().all():
                new_essence = account.seasonal_points + account.seasonal_earned
                print(f'- {account.account_name}: {account.seasonal_points} existing + ' \
                    f'{account.seasonal_earned} earned = {new_essence} essence')
                account.seasonal_points = new_essence

                for del_player in account.players:
                    if not del_player.is_immortal:
                        del_id      = del_player.id
                        del_path    = f'{PODIR}/{del_player.name}'
                        print(f'    - {del_player.name} ({del_path})')
                        db_session.query(models.PlayersFlag).filter_by(
                            player_id = del_id
                        ).delete()
                        db_session.query(models.PlayerQuest).filter_by(
                            player_id = del_id
                        ).delete()
                        db_session.query(models.PlayerRemortUpgrade).filter_by(
                            player_id = del_id
                        ).delete()
                        db_session.query(models.Player).filter_by(
                            id = del_id
                        ).delete()

                        # Append the player Podir file name to be deleted, if it exists
                        if os.path.exists(del_path):
                            podir_del.append(del_path)

            confirm_pwipe = input('\nIs this OK?\nCAUTION: All mortals will be wiped!\n' \
                                'Type "YES" to commit the changes: ')
            print('\n')

            if confirm_pwipe == 'YES':
                for podir_file in podir_del:
                    if os.remove(podir_file):
                        print(f'Deleted: {podir_file}')
                db_session.commit()
                finish(code=0, message='Player wipe complete')

        # List Active
        elif opt in ('-l', '--list'):
            seasons = models.Season.query.filter_by(is_active=1).all()
            if seasons:
                for season in seasons:
                    print(season)
                finish(code=0, message='')
            else:
                finish(code=1, message='No active seasons')

        # List All
        elif opt in ('--list-all'):
            seasons = models.Season.query.order_by(models.Season.season_id).all()
            if seasons:
                for season in seasons:
                    print(season)
                finish(code=0, message='')
            else:
                finish(code=1, message='No active seasons')

        # Invalid options
        else:
            assert False, 'Invalid option'

    # Show usage if there are no options
    if len(sys.argv) <= 1:
        usage()
        finish(code=0, message='')

    # Exit
    finish()
