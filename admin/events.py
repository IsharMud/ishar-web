"""Admin Events"""
from flask import abort, Blueprint, flash, render_template, url_for
from flask_login import current_user, fresh_login_required

from database import db_session
from forms import EventAddForm
from models.globalevent import GlobalEvent


# Flask Blueprint
admin_events_bp = Blueprint(
    'admin_events',
    __name__,
    url_prefix='/events',
    template_folder='templates/events'
)


@admin_events_bp.before_request
@fresh_login_required
def before_request():
    """Only Gods can access /admin/events"""
    if not current_user.is_god:
        flash('Sorry, but you are not godly enough (Gods only)!', 'error')
        abort(401)


@admin_events_bp.route('/', methods=['GET', 'POST'])
def index():
    """Administration portal to allow Gods to add global events
        /admin/events"""

    # Get event add form and check if submitted
    event_add_form = EventAddForm()
    if event_add_form.validate_on_submit():

        # Create the new global event database entry
        new_global_event = GlobalEvent(
            event_type=event_add_form.event_type.data,
            start_time=event_add_form.start_time.data,
            end_time=event_add_form.end_time.data,
            event_name=event_add_form.event_name.data,
            event_desc=event_add_form.event_desc.data,
            xp_bonus=event_add_form.xp_bonus.data,
            shop_bonus=event_add_form.shop_bonus.data,
            celestial_luck=event_add_form.celestial_luck.data
        )
        db_session.add(new_global_event)
        db_session.commit()
        edit_url = url_for(
            '.edit',
            edit_event_type=new_global_event.event_type
        )
        flash(
            'The global event was added! '
            f'You can <a href="{edit_url}">edit it here</a>.',
            'success'
        )

    # Show the form to manage global events in the administration portal
    return render_template(
        'events.html.j2',
        all_events=GlobalEvent.query.all(),
        event_add_form=event_add_form
    )


@admin_events_bp.route('/edit/<int:edit_event_type>/', methods=['GET', 'POST'])
@admin_events_bp.route('/edit/<int:edit_event_type>', methods=['GET', 'POST'])
def edit(edit_event_type=None):
    """Administration portal to allow Gods to edit global events
        /admin/events/edit"""
    event = GlobalEvent.query.filter_by(event_type=edit_event_type).first()
    if not event:
        flash('Invalid global event.', 'error')
        abort(400)

    # Get event form, and check if submitted
    edit_event_form = EventAddForm()
    if edit_event_form.validate_on_submit():
        event.event_type = edit_event_form.event_type.data
        event.start_time = edit_event_form.start_time.data
        event.end_time = edit_event_form.end_time.data
        event.event_name = edit_event_form.event_name.data
        event.event_desc = edit_event_form.event_desc.data
        event.xp_bonus = edit_event_form.xp_bonus.data
        event.shop_bonus = edit_event_form.shop_bonus.data
        event.celestial_luck = edit_event_form.celestial_luck.data
        db_session.commit()
        flash('The global event was saved.', 'success')

    return render_template(
        'edit_event.html.j2',
        edit_event=event,
        edit_event_form=edit_event_form
    )


@admin_events_bp.route('/delete/<int:delete_event_type>/', methods=['GET'])
@admin_events_bp.route('/delete/<int:delete_event_type>', methods=['GET'])
def delete(delete_event_type=None):
    """Administration portal to allow Gods to delete global events
        /admin/events/delete"""
    event = GlobalEvent.query.filter_by(event_type=delete_event_type).first()
    if not event:
        flash('Invalid global event.', 'error')
        abort(400)

    GlobalEvent.query.filter_by(event_type=event.event_type).delete()
    db_session.commit()
    flash('The global event was deleted.', 'success')

    # Show the form to add global events in the administration portal
    return index()
