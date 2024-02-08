"""
WSGI config for sitaram project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

HOME = os.environ['HOME']
CODE_PATH = f'{HOME}/sitaram'

if CODE_PATH not in sys.path:
    sys.path.insert(0, CODE_PATH)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sitaram.settings')
os.environ.setdefault('SECRET_KEY', 'nbvFD^sg-jsh^gjer4ds3fsd#s$sd*gsfvsjhas')
os.environ.setdefault('FAST_SMS_AUTH_KEY', 'nbvFD^sg-jsh^gjer4ds3fsd#s$sd*gsfvsjhas')

application = get_wsgi_application()
