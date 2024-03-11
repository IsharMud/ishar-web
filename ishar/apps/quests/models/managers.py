from django.db.models import Manager


class QuestManager(Manager):

    def get_by_natural_key(self, display_name):
        # Natural key by quest display name.
        return self.get(display_name=display_name)
