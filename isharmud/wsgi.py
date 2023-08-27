"""
WSGI config for isharmud.com project.
"""
import os
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isharmud.settings')
application = get_wsgi_application()
