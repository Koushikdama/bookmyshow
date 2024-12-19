"""
WSGI config for bookmyseat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application
# from django.core.wsgi import get_wsgi_application
# from django.contrib.staticfiles.handlers import StaticFilesHandler

# application = StaticFilesHandler(get_wsgi_application())

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyseat.settings')

# application = get_wsgi_application()
# app = application


import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyseat.settings')

application = get_wsgi_application()

# Vercel requires a variable named `app` or `handler`
app = application

