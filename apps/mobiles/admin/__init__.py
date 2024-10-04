from django.contrib.admin import site

from ..models.mobile import Mobile
from .mobile import MobileAdmin


site.register(Mobile, MobileAdmin)
