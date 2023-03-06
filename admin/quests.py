"""Admin Quests"""
from flask import abort, Blueprint, flash, render_template, url_for

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
    quest_add_form = QuestForm()
    if quest_add_form.validate_on_submit():

        # Create the new quest database entry
        new_quest = Quest(
            name=quest_add_form.name.data,
            display_name=quest_add_form.display_name.data,
            completion_message=quest_add_form.completion_message.data,
            min_level=quest_add_form.min_level.data,
            max_level=quest_add_form.max_level.data,
            repeatable=quest_add_form.repeatable.data,
            description=quest_add_form.description.data,
#            prerequisite=quest_add_form.prerequisites.data,
#            class_restrict=quest_add_form.class_restrict.data,
            quest_intro=quest_add_form.quest_intro.data
        )
        db_session.add(new_quest)
        db_session.commit()
        edit_url = url_for('.edit', edit_quest_id=new_quest.quest_id)
        flash(f'The quest was added! You can <a href="{edit_url}">edit it here</a>.', 'success')

    # Show the form to manage quests in the administration portal
    return render_template(
        'quests.html.j2',
        all_quests=Quest.query.order_by(-Quest.quest_id).all(),
        quest_form=quest_add_form
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
        edit_quest.name = edit_quest_form.name.data
        edit_quest.display_name = edit_quest_form.display_name.data
        edit_quest.completion_message = edit_quest_form.completion_message.data
        edit_quest.min_level = edit_quest_form.min_level.data
        edit_quest.max_level = edit_quest_form.max_level.data
        edit_quest.repeatable = edit_quest_form.repeatable.data
        edit_quest.description = edit_quest_form.description.data
        edit_quest.class_restrict = edit_quest_form.class_restrict.data
        edit_quest.quest_intro = edit_quest_form.quest_intro.data
        edit_quest.prerequisites = edit_quest_form.prerequisites.data
        db_session.commit()
        flash('The quest was saved.', 'success')

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
