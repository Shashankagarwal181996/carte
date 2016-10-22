"""
WSGI config for carte project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carte.settings")

# application = get_wsgi_application()

# from whitenoise.django import DjangoWhiteNoise
# application = DjangoWhiteNoise(application)
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carte.settings")

# This application object is used by the development server
# as well as any WSGI server configured to use this file.

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# import django.core.handlers.wsgi
# application = django.core.handlers.wsgi.WSGIHandler()