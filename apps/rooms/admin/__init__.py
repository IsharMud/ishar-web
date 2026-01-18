from django.contrib.admin import site

from ..models.room import Room
from .room import RoomAdmin


site.register(Room, RoomAdmin)
