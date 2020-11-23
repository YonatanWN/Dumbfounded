"""Name: urls.py
Purpose: determines url patterns, and sets which functions in views.py handle those url patterns
Version: Added documentation, June 9th 2020
Authors:  Luke Patton
Dependecies: python, django"""

from django.urls import path

from . import views

app_name='game'

urlpatterns = [
    path('new/', views.landingpage, name='new'),
    path('gameroom/', views.gameroom, name='gameroom'),
    path('<str:roomcode>/', views.gameroom, name='gameroom'),
    
]
