#!/usr/bin/env python3
import datetime
from database import db_session
import models
import sentry_sdk
import sentry_secret

sentry_sdk.init(dsn=sentry_secret.DSN, traces_sample_rate=1.0)

SEPARATOR   = '~-=-=-=-~=~-=-=-=-~'

print('IsharMUD Season Manager\n')
print(SEPARATOR)

NOW     = datetime.datetime.utcnow()
CREATE  = False

active_seasons  = models.Season.query.filter_by(
                    is_active   = 1
                ).order_by(
                    -models.Season.season_id
                ).all()

print(f'The current time is:')
print(NOW.strftime('%A, %B %d, %Y @ %H:%M:%S %Z'))
print(NOW)
print(SEPARATOR)

if len(active_seasons) == 0:
    print("There are NO active seasons in the database! \n")
    CREATE  = True

elif len(active_seasons) == 1:
    current_season  = active_seasons[0]
    print(f"The current season is: {current_season.season_id}")
    print(f" - Started: {current_season.effective_date} ({current_season.effective})")
    print(f" - Expires: {current_season.expiration_date} ({current_season.expires})\n")

    confirm_expire  = input('Do you want to expire the current season ' \
                        f"(season {current_season.season_id}) now? ")
    print("\n")
    if confirm_expire.lower() == 'yes' or confirm_expire.lower() == 'y':
        current_season.expire(expire_when=NOW)
        expired_season  = models.Season.query.filter_by(
                            season_id   = current_season.season_id
                        ).first()
        print(f"Season EXPIRED: {expired_season.season_id}")
        print(f" - Started: {expired_season.effective_date} ({expired_season.effective})")
        print(f" - Expired: {expired_season.expiration_date} ({expired_season.expires})\n")
        CREATE  = True

elif len(active_seasons) > 1:
    print("There are multiple active seasons in the database! ")
    print("Expiring all and starting fresh... \n")
    for active_season in active_seasons:
        active_season.expire(expire_when=NOW)
    CREATE  = True

print(SEPARATOR)

if CREATE:
    print('Creating new season...')
    create_length   = input('How long will the season be in months? [default: 4] ') or 4
    created_id      = models.Season().create(start_when=NOW, length_months=int(create_length))
    created_season  = models.Season.query.filter_by(season_id = created_id).first()
    print(f"The new season is: {created_season.season_id} ")
    print(f" - Started: {created_season.effective_date} ({created_season.effective})")
    print(f" - Expires: {created_season.expiration_date} ({created_season.expires})")
    print(SEPARATOR)

confirm_pwipe   = input("Do you want to WIPE ALL PLAYERS from the database?\n" \
                    "This will calculate all account essence earned and apply it.\n" \
                    'CAUTION!!! Enter "YES" to confirm: ')
print("\n")

if confirm_pwipe == 'YES':
    print(SEPARATOR)
    print('OK.... \n')
    accounts    = models.Account.query.filter().all()
    for account in accounts:
        new_total   = account.seasonal_points + account.seasonal_earned
        print(f'- {account.account_name}:\n' \
            f'  -> {account.seasonal_points} existing + {account.seasonal_earned} earned\n' \
            f'  --> {new_total} essence')
        print('  + Deleting... ')
        for del_player in account.players:
            if not del_player.is_immortal:
                print(f'    - {del_player.name}')
                # TODO: Delete Podir file on disk in the MUD directory
                # ...and announce the p-wipe in Discord or something maybe?
                db_session.query(models.PlayersFlag).filter_by(player_id = del_player.id).delete()
                db_session.query(models.PlayerQuest).filter_by(player_id = del_player.id).delete()
                db_session.query(models.PlayerRemortUpgrade).filter_by(player_id = del_player.id).delete()
                db_session.query(models.Player).filter_by(id = del_player.id).delete()

    final_confirm   = input('\nIs this OK? Type "YES" to commit the changes: ')
    if final_confirm == 'YES':
        db_session.commit()
        print('\nWIPED!\n')

print(SEPARATOR)
print("Have a lovely day!\n")

db_session.close()
