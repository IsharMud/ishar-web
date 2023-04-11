"""Admin Quests"""
from flask import abort, Blueprint, flash, render_template, url_for
from flask_login import current_user, fresh_login_required

from database import db_session
from models.forms import QuestForm
from models.player.common import Class
from models.quest import Quest


# Flask Blueprint
admin_quests_bp = Blueprint(
    'admin_quests',
    __name__,
    url_prefix='quests',
    template_folder='templates/quests'
)


@admin_quests_bp.before_request
@fresh_login_required
def before_request():
    """Only Eternals and above can access /admin/quests"""
    if not current_user.is_eternal:
        flash(
            'Sorry, but you are not godly enough (Eternals and above only)!',
            'error'
        )
        abort(401)


@admin_quests_bp.route('/', methods=['GET', 'POST'])
def index():
    """Administration portal to allow Gods to manage quests
        /admin/quests"""

    # Get quest form
    add_quest_form = QuestForm()

    # Retrieve playable player class names for form choices
    playable_classes = Class().query.filter(
        Class.class_description != ''
    ).all()
    for playable_class in playable_classes:
        add_quest_form.class_restrict.choices.append(
            (playable_class.class_id, playable_class.class_display_name)
        )

    # Check if quest add form submitted
    if add_quest_form.validate_on_submit():

        # Create the new quest database entry
        new_quest = Quest(
            name=add_quest_form.name.data,
            display_name=add_quest_form.display_name.data,
            completion_message=add_quest_form.completion_message.data,
            min_level=add_quest_form.min_level.data,
            max_level=add_quest_form.max_level.data,
            repeatable=add_quest_form.repeatable.data,
            description=add_quest_form.description.data,
            prerequisite=add_quest_form.prerequisite.data,
            class_restrict=add_quest_form.class_restrict.data,
            quest_intro=add_quest_form.quest_intro.data
        )
        db_session.add(new_quest)
        db_session.commit()
        flash(
            'The quest was added! You can <a href="'
            f"{url_for('.edit', edit_quest_id=new_quest.quest_id)}"
            '">edit it here</a>.',
            'success'
        )

    # Show the form to manage quests in the administration portal
    return render_template(
        'quests.html.j2',
        all_quests=Quest.query.order_by(-Quest.quest_id).all(),
        quest_form=add_quest_form
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

    # Retrieve playable player class names for form choices
    player_classes = Class().query.filter(Class.class_description != '').all()
    for player_class in player_classes:
        edit_quest_form.class_restrict.choices.append(
            (player_class.class_id, player_class.class_display_name)
        )
    edit_quest_form.class_restrict.default = edit_quest.class_restrict

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
        edit_quest.prerequisite = edit_quest_form.prerequisite.data
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
    flash(
        f'The quest ({delete_quest.name} [ID: {delete_quest.quest_id}]) '
        'was deleted.',
        'success'
    )

    # Show the form to manage quests in the administration portal
    return index()
