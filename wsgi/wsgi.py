"""
WSGI config for costruttoridimondi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(os.path.abspath(os.path.join(BASE_DIR, 'costruttoridimondi')))

print(sys.path[-1])

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "costruttoridimondi.settings")

application = get_wsgi_application()
