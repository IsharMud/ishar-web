"""Admin Quests"""
from flask import abort, Blueprint, flash, render_template

from database import db_session
from forms import QuestForm
from models import Quest


# Flask Blueprint
admin_quests_bp = Blueprint(
    'admin_quests',
    __name__,
    url_prefix='quests',
    template_folder='templates/quests'
)


@admin_quests_bp.route('/', methods=['GET', 'POST'])
def index():
    """Administration portal to allow Gods to manage quests
        /admin/quests"""

    # Get quest form and check if submitted
    flash('Quest administration is a work in progress...', 'warning')
    quest_form = QuestForm()
    if quest_form.validate_on_submit():
        flash('The quest form is still under construction!', 'error')

    # Show the form to manage quests in the administration portal
    return render_template(
        'quests.html.j2',
        all_quests=Quest.query.all(),
        quest_form=quest_form
    )


@admin_quests_bp.route('/edit/<int:edit_quest_id>/', methods=['GET', 'POST'])
@admin_quests_bp.route('/edit/<int:edit_quest_id>', methods=['GET', 'POST'])
def edit(edit_quest_id=None):
    """Administration portal to allow Gods to edit quests
        /admin/quests/edit"""
    edit_quest = Quest.query.filter_by(quest_id=edit_quest_id).first()
    if not edit_quest:
        flash('Invalid quest.', 'error')
        abort(400)

    # Get quest form, and check if submitted
    edit_quest_form = QuestForm()
    if edit_quest_form.validate_on_submit():
        db_session.commit()
        flash('The quest form is still under construction!', 'error')

    return render_template(
        'edit_quest.html.j2',
        edit_quest=edit_quest,
        edit_quest_form=edit_quest_form
    )


@admin_quests_bp.route('/delete/<int:delete_quest_id>/', methods=['GET'])
@admin_quests_bp.route('/delete/<int:delete_quest_id>', methods=['GET'])
def delete(delete_quest_id=None):
    """Administration portal to allow Gods to delete quests
        /admin/quest/delete"""
    delete_quest = Quest.query.filter_by(quest_id=delete_quest_id).first()
    if not delete_quest:
        flash('Invalid quest.', 'error')
        abort(400)

    Quest.query.filter_by(quest_id=delete_quest.quest_id).delete()
    db_session.commit()
    flash(f'The quest ({delete_quest.name} [ID: {delete_quest.quest_id}]) was deleted.', 'success')

    # Show the form to manage quests in the administration portal
    return index()
