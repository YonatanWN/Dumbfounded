"""Name: apps.py
Purpose: Tells django what the name of this app is (auto created)
Version: Added documentation, June 9th 2020
Authors:  Luke Patton
Dependecies: python, django"""

from django.apps import AppConfig


class GameConfig(AppConfig):
    name = 'game'
