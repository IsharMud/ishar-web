"""Admin Seasons"""
import os
from datetime import datetime

from flask import Blueprint, flash, render_template

from mud_secret import IMM_LEVELS
from database import db_session
from forms import SeasonCycleForm
from models import Account, Player, Season
from sentry import sentry_sdk


# Flask Blueprint
seasons = Blueprint(
    'seasons',
    __name__,
    url_prefix='/seasons',
    template_folder='templates/seasons'
)


@seasons.route('/', methods=['GET'])
def index():
    """Administration portal to allow Gods to view/manage seasons
        /admin/seasons"""
    return render_template(
        'seasons.html.j2',
        seasons=Season.query.order_by(
            -Season.is_active,
            -Season.season_id
        ).all()
    )


@seasons.route('/cycle/', methods=['GET', 'POST'])
@seasons.route('/cycle', methods=['GET', 'POST'])
def cycle():
    """Administration portal to allow Gods to cycle seasons,
        while wiping players - /admin/seasons/cycle"""

    # Get season cycle form, and check if submitted
    season_cycle_form = SeasonCycleForm()
    if season_cycle_form.validate_on_submit():

        # Expire any existing active seasons
        for active_season in Season.query.filter_by(is_active=1).all():
            active_season.is_active = 0
            active_season.expiration_date = datetime.utcnow()
            flash(f'Season {active_season.season_id} expired.', 'success')
            sentry_sdk.capture_message(f'Season Expired: {active_season}')

        # Create the new season database entry
        new_season = Season(
            is_active=1,
            effective_date=season_cycle_form.effective_date.data,
            expiration_date=season_cycle_form.expiration_date.data
        )
        db_session.add(new_season)

        # Loop through all accounts
        total_ess = total_fdelete = total_pdelete = total_immskip = 0
        for account in Account.query.filter().all():

            # Apply any essence earned
            if account.seasonal_earned > 0:

                # Add existing essence plus essence earned
                calc = account.seasonal_points + account.seasonal_earned
                flash(
                    f'Account "{account.display_name}" '
                    f'({account.account_id}) '
                    f'now has {calc} essence. '
                    f'({account.seasonal_points} existing + '
                    f'{account.seasonal_earned} earned)',
                    'success'
                )

                # Update account essence balance in the database,
                #   along with running total
                account.seasonal_points = calc
                total_ess += calc

            # Mention accounts that earned no essence
            else:
                flash(
                    f'Account "{account.display_name}" ({account.account_id})'
                    ' earned no essence', 'info'
                )

            # Loop through each player in each account
            for delete_player in account.players:

                # Skip immortal players
                if delete_player.is_immortal:
                    flash(f'Immortal: {delete_player.display_name}', 'info')
                    total_immskip += 1
                    continue

                # Delete player from the database
                Player.query.filter_by(id=delete_player.id).delete()

                # Check that player Podir file exists on disk, and remove
                if os.path.isfile(delete_player.podir):
                    os.remove(delete_player.podir)
                    total_fdelete += 1
                    flash(
                        f'Deleted Podir: <code>{delete_player.podir}</code>!',
                        'success'
                    )

                # Warn if no Podir file exists for the player
                else:
                    flash(
                        f'Missing Podir: <code>{delete_player.podir}</code>',
                        'warn'
                    )
                total_pdelete += 1

        db_session.commit()
        flash(f'All ({total_ess}) essence has been rewarded.', 'success')
        sentry_sdk.capture_message(f'Essence Rewarded: {total_ess} essence')

        # Make sure a season was created
        if new_season.season_id:
            flash(f'Season {new_season.season_id} created.', 'success')
            sentry_sdk.capture_message(f'Season Created: {new_season}')

        # Make sure that only immortals remain
        flash(f'A total of {total_pdelete} mortals were wiped.', 'success')
        flash(f'A total of {total_immskip} immortals skipped.', 'info')
        if not Player.query.filter(Player.true_level < min(IMM_LEVELS)).all():
            flash('Only immortals remain.', 'success')

    # Show the form to cycle a season in the administration portal
    return render_template(
        'cycle.html.j2',
        season_cycle_form=season_cycle_form
    )
