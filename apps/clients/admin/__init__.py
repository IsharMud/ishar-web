from django.contrib.admin import site

from ..models.category import MUDClientCategory
from ..models.client import MUDClient

from .category import MUDClientCategoryAdmin
from .client import MUDClientAdmin


site.register(MUDClientCategory, MUDClientCategoryAdmin)
site.register(MUDClient, MUDClientAdmin)
