"""
WSGI config for speakez project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'speakez.settings')

application = get_wsgi_application()


import ptvsd

try:
    ptvsd.enable_attach("my_secret", address=('localhost', 3000))
except:
    pass