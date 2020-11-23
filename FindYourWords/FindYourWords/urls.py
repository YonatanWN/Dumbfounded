"""Name: urls.py
Purpose: routes url patterns. Since we have only one app, it points all traffic to that app.
Version: Added documentation, June 9th 2020
Authors:  Luke Patton
Dependecies: python, django"""
from django.contrib import admin
from django.urls import path, include
from game import views

urlpatterns = [
    path('game/', include('game.urls')),
    # traffic to base url is redirected to game url
    path('', views.redirect_view),
]
