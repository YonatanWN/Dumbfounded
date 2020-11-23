"""Name: wsgi.py
Purpose: Declares the asgi application for our web app
Version: Added documentation, June 9th 2020
Authors:  Luke Patton
Dependecies: python, django, django channels"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FindYourWords.settings')

application = get_wsgi_application()
