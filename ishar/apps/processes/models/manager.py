from django.db.models import Manager
from os import getlogin


class MUDProcessManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user__exact=getlogin())
