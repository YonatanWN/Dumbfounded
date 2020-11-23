"""Name: routing.py
Purpose: Declares the url routing for our websocket
Version: Added documentation, June 9th 2020
Authors:  Luke Patton
Dependecies: python, django, django channels"""

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import game.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(game.routing.websocket_url_patterns)
    ),
})
