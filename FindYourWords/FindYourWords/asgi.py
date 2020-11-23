"""Name: asgi.py
Purpose: Declares the asgi application for our web app. Used by django.
Version: Added documentation, June 9th 2020
Authors:  Luke Patton
Dependecies: python, django"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FindYourWords.settings')

application = get_asgi_application()
