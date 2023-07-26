"""Admin Seasons"""
import os
from datetime import datetime

from flask import abort, Blueprint, flash, render_template
from flask_login import current_user, fresh_login_required

from config import IMM_LEVELS
from database import db_session
from forms import SeasonCycleForm
from models.account import Account
from models.player import Player
from models.season import Season
from sentry import sentry_sdk


# Flask Blueprint
admin_seasons_bp = Blueprint(
    'admin_seasons',
    __name__,
    url_prefix='/seasons',
    template_folder='templates/seasons'
)


@admin_seasons_bp.before_request
@fresh_login_required
def before_request():
    """Only Gods can access /admin/seasons"""
    if not current_user.is_god:
        flash('Sorry, but you are not godly enough (Gods only)!', 'error')
        abort(401)


@admin_seasons_bp.route('/', methods=['GET'])
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


@admin_seasons_bp.route('/cycle/', methods=['GET', 'POST'])
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

        # Prepare to count player wipe statistics
        wipe_totals = {
            'accounts': 0,
            'essence': 0,
            'immortals': 0,
            'players': 0,
            'podirs': 0
        }

        # Loop through each account
        for account in Account.query.filter().all():
            wipe_totals['accounts'] += 1

            # Apply any essence earned
            if account.seasonal_earned > 0:
                wipe_totals['essence'] += account.seasonal_earned
                calc = account.current_essence + account.seasonal_earned
                account.current_essence = calc
                flash(
                    f'Account "{account.display_name}" ({account.account_id}) '
                    f'now has {calc} essence. '
                    f'({account.current_essence} existing + '
                    f'{account.seasonal_earned} earned)', 'success')

            # Loop through each player in each account
            for delete_player in account.players:

                # Skip immortal players
                if delete_player.is_immortal:
                    wipe_totals['immortals'] += 1
                    flash(f'Immortal: {delete_player.name}', 'info')
                    continue

                # Delete player from the database
                wipe_totals['players'] += 1
                Player.query.filter_by(id=delete_player.id).delete()

                # Check that player Podir file exists on disk, and remove
                if os.path.isfile(delete_player.podir):
                    wipe_totals['podirs'] += 1
                    os.remove(delete_player.podir)
                    flash(
                        f'Deleted: <code>{delete_player.podir}</code>',
                        'success')

        # Write database changes
        db_session.commit()

        # Display statistics
        for wipe_type, wipe_count in wipe_totals.items():
            flash(f'Total {wipe_type.title()}: {wipe_count}', 'info')

        # Check that the new season got an ID, meaning it was created
        if new_season.season_id:
            flash(f'Season {new_season.season_id} created', 'success')
            sentry_sdk.capture_message(f'Season Created: {new_season}')

        # Check that only immortals remain
        if not Player.query.filter(Player.true_level < min(IMM_LEVELS)).all():
            flash('Player wipe complete! Only immortals remain.', 'success')
        else:
            flash('Something went wrong! More than immortals remain.', 'error')

    # Show the form to cycle a season in the administration portal
    return render_template(
        'cycle.html.j2',
        season_cycle_form=season_cycle_form
    )
