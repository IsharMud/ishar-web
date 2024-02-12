from django.urls import reverse
from django.utils.html import format_html

from .quest import QuestAdmin
from .reward import QuestRewardAdmin


def get_quest_class_link(obj=None) -> (str, None):
    if obj and obj.get_class_restrict_display() is not None:
        return format_html(
            '<a href="%s">%s</a>' % (
                reverse(
                    viewname="admin:classes_class_change",
                    args=(obj.class_restrict,)
                ),
                obj.get_class_restrict_display()
            )
        )
    return None


def get_quest_name_link(obj=None) -> (str, None):
    if obj is not None:
        return format_html(
            '<a href="%s">%s</a>' % (
                reverse(
                    viewname="admin:quests_quest_change",
                    args=(obj.quest.quest_id,)
                ),
                obj.quest.display_name
            )
        )
    return None
