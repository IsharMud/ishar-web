#!/usr/bin/env python3
"""
Manage seasons for IsharMUD via CLI
Optionally expire the season and/or erase mortal players
"""
import datetime
import os
import sentry_sdk
from database import db_session
import models
import sentry_secret

# Set up sentry
sentry_sdk.init(dsn=sentry_secret.DSN, traces_sample_rate=1.0)

# Pretty separator line and header with current time
SEPARATOR   = '~-=-=-=-~=~-=-=-=-~=~-=-=-=-~=~-=-=-=-~'
print('IsharMUD Season Manager\n')
print(SEPARATOR)
NOW = datetime.datetime.utcnow()
print(f"{NOW.strftime('%A, %B %d, %Y @ %H:%M:%S %Z')}\n{NOW}")
print(SEPARATOR)

# Do not create a new season by default
CREATE  = False

# Find any active seasons
active_seasons  = models.Season.query.filter_by(
                    is_active   = 1
                ).order_by(
                    -models.Season.season_id
                ).all()

def display_season(season=active_seasons[0]):
    """Method to display the details of a season"""
    print(f'SEASON {season.season_id} / ' \
        f'Effective: {season.effective_date} ({season.effective}) / ' \
        f'Expiration: {season.expiration_date} ({season.expires})')


# Create new season if there are none active
if len(active_seasons) == 0:
    print('There are NO active seasons in the database! Creating a new season.')
    CREATE  = True

# Normal state is a single active season
elif len(active_seasons) == 1:

    # Display current active season details
    current_season  = active_seasons[0]
    print('CURRENT: ')
    display_season(season=current_season)

    # Prompt to expire the current season
    confirm_expire  = input('Do you want to expire the current season ' \
                        f'(season {current_season.season_id}) NOW? [n] ')
    print('\n')

    # Expire the current season if requested, and start new season
    if confirm_expire.lower() == 'yes' or confirm_expire.lower() == 'y':
        current_season.expire(expire_when=NOW)
        expired_season  = models.Season.query.filter_by(
                            season_id   = current_season.season_id
                        ).first()
        print('EXPIRED: ')
        display_season(season=expired_season)
        CREATE  = True

# More than one active season is invalid so expire all, and start new season
elif len(active_seasons) > 1:
    print('There are multiple active seasons in the database!' \
        'Expiring all active seasons, and creating a new season.')
    for active_season in active_seasons:
        active_season.expire(expire_when=NOW)
    CREATE  = True

# Create a new season if needed
print(SEPARATOR)
if CREATE:
    print('Creating new season...')

    # Prompt for the length of the season in months, defaulting to 4 months
    create_length   = input('How long will the season be (in months)? [4] ') or 4

    # Add the new season to the database and check that it worked
    created_id      = models.Season().create(start_when=NOW, length_months=int(create_length))
    created_season  = models.Season.query.filter_by(season_id = created_id).first()

    # Display newly created active season details
    print('CREATED: ')
    display_season(season=created_season)
else:
    print('Skipping new season creation...')

# Prompt to determine if a player-wipe should be performed
print(SEPARATOR)
do_pwipe    = input('Do you want to perform a player wipe?\n' \
                    'This will calculate all account essence earned and apply it.\n' \
                    'You will have a final chance to confirm, before players are wiped.\n' \
                    'Proceed? [n] ')
print('\n')
print(SEPARATOR)

# Start processing potentional player wipe, if requested
if do_pwipe.lower() == 'yes' or do_pwipe.lower() == 'y':
    print('Calculating player wipe... \n')

    # Find all accounts and set up an empty list of Podir files to delete
    accounts    = models.Account.query.filter().all()
    podir_del   = []
    PODIR       = '/home/ishartest/ishar-mud/lib/Podir'

    # Loop through each account
    for account in accounts:

        # Determine the new total essence for the account
        new_essence = account.seasonal_points + account.seasonal_earned
        print(f'- {account.account_name}: {account.seasonal_points} existing + ' \
            f'{account.seasonal_earned} earned = {new_essence} essence')
        account.seasonal_points =   new_essence

        # Loop through each (non-immortal) player within the account
        for del_player in account.players:
            if not del_player.is_immortal:
                print(f'    - {del_player.name}')
                del_id      = del_player.id
                del_path    = f'{PODIR}/{del_player.name}'

                # Remove the players flags, quests, remort upgrades,
                # ...and finally the player itself
                db_session.query(models.PlayersFlag).filter_by(player_id = del_id).delete()
                db_session.query(models.PlayerQuest).filter_by(player_id = del_id).delete()
                db_session.query(models.PlayerRemortUpgrade).filter_by(player_id = del_id).delete()
                db_session.query(models.Player).filter_by(id = del_id).delete()

                # Append the player Podir file name to be deleted, if it exists
                if os.path.exists(del_path):
                    podir_del.append(del_path)

    # Prompt for final confirmation of player wipe
    confirm_pwipe   = input('\nIs this OK?\nCAUTION: All mortals will be wiped!\n' \
                        'Type "YES" to commit the changes: ')
    print('\n')

    # Delete each "Podir" file and commit the database changes wiping players
    print(SEPARATOR)
    if confirm_pwipe == 'YES':
        for podir_file in podir_del:
            print('Deleted Podir file ({podir_file})')
            os.remove(podir_file)
        db_session.commit()
        print('\nWIPED!\n')

    else:
        print('Skipping player wipe at final confirmation... \n')
else:
    print('Skipping player wipe... \n')

print(SEPARATOR)
print('Good bye!\n')

db_session.close()
