"""Name: consumers.py
Purpose: Manages WebSocket connections to enable front-end back-end communication
Version: Added documentation, June 9th 2020
Authors:  Luke Patton
Dependecies: python, django, django channels"""

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from game.models import BoardPosition, Player, Game
import json
from datetime import datetime
import pytz

# Subclass of Django Channels' Websocket Consumer.
# This will manage messages being sent to and from the backend
class RoomConsumer(WebsocketConsumer):
    # this gets called whenever a new computer joins a game
    def connect(self):
        # get room code from info sent
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.player_id = self.scope['url_route']['kwargs']['pk']
        
        #find the player associated with that id and mark the player as currently connected
        p = Player.objects.filter(pk=self.player_id)[0]
        p.connected = True
        p.save()
        
        # set up the romm group
        self.room_group = "group_for_" + str(self.room_code)
        async_to_sync(self.channel_layer.group_add)(self.room_group, self.channel_name)
        
        self.accept()
        
    
    #this is called whenever a player disconnects (usually because their window was closed)
    def disconnect(self, close_code):
        # leave room
        async_to_sync(self.channel_layer.group_discard)(self.room_group, self.channel_name)
        try:
            #mark the player as disconnected so they can later rejoin
            p = Player.objects.filter(pk=self.player_id)[0]
            p.connected = False
            p.save()
        except:
            print("a player disconnected")
    
    # this is called when we get a message from the frontend
    def receive(self, text_data):

        
        json_data = json.loads(text_data)
        
        
        
        if json_data['type'] == 'button':
            # the message was a button press
            
            # get the coordinates of the button from the data sent from front end
            x = json_data['x']
            y = json_data['y']
            
            
            r = Game.objects.filter(room_code=self.room_code)[0]
            
            # handle backend of button position
            bp = BoardPosition.objects.filter(x=x, y=y, game=r)[0]
            if not bp.revealed:
                # mark the button as being revealed
                bp.revealed = True
            
                team = bp.team
                bp.save()
                
                # send message to whole group so their buttons get marked as pressed
                message = {'type': 'button_press',
                        'message_type': 'button_press',
                        'x': x,
                        'y': y,
                        'team': team
                }
                
                async_to_sync(self.channel_layer.group_send)(self.room_group, message)
                
                if (int(team) == 1 and int(r.team_turn) == 2) or (int(team) == 2 and int(r.team_turn) == 1):
                    #if the button clicked was on the team whose turn it is, decrease the words_left in the current game
                    r.words_left -= 1
                elif team == 0 or team == -1 or int(team) ==  int(r.team_turn):
                    #if the button clicked was neutral, assassin, or the other team, end the current clue by setting words_left to 0
                    r.words_left = 0
                    
                    #if the team was -1 (assassin/bomb), that team loses
                    if team == -1:
                        async_to_sync(self.channel_layer.group_send)(self.room_group, {'type': 'win', 'team' : 1 if r.team_turn == 2 else 2})
                        
                
                    
                r.save()
                
                if r.words_left == 0:
                    #if words_left is 0, reset the clue and team turn.
                    r.current_clue = ""
                    r.team_turn = 1 if r.team_turn == 2 else 2
                    r.save()
                    async_to_sync(self.channel_layer.group_send)(self.room_group, {'type': 'turn', 'message_type': 'turn', 'team': r.team_turn})
                    
                    #update time so no current timer
                    self.updateTime(False)
                #check to see if someone has won by looping through all the boardpositions, to see if a team has run out of clues.
                
                team_1_card_count = 0
                team_2_card_count = 0
                
                for bp in r.boardposition_set.all():
                    if bp.team == 1 and not bp.revealed:
                        team_2_card_count += 1
                    elif bp.team == 2 and not bp.revealed:
                        team_1_card_count += 1
                        
                if team_1_card_count == 0:
                    async_to_sync(self.channel_layer.group_send)(self.room_group, {'type': 'win', 'team' : '1'})
                elif team_2_card_count == 0:
                    async_to_sync(self.channel_layer.group_send)(self.room_group, {'type': 'win', 'team' : '2'})
                    
                
                #update the clue
                async_to_sync(self.channel_layer.group_send)(self.room_group, {'type': 'clue', 'message_type': 'clue', 'word': r.current_clue, 'num': r.words_left})
                
                
        elif json_data['type'] == 'player':
            # a player joined
            
            pk = json_data['pk']
            
            #find which player it is
            p = Player.objects.filter(pk=pk)[0]
            if not p.room_alerted:
                # Tell the group that a new player has been added
                # we only want this to happen once for each player (i.e. we don't want it to happen if they reload the page, so we track for each player whether they have sent this or not
                message = {
                    'type': 'player',
                    'message_type': 'player',
                    'name': p.name,
                    'team': p.team,
                    'captain?': p.captain,
                    'avatar': p.avatar_num}
                async_to_sync(self.channel_layer.group_send)(self.room_group, message)
                p.room_alerted = True
                p.save()
                
        elif json_data['type'] == 'clue':
            # a clue was given, almost all we have to do is send it back out to everyone
            
            # first we mark the clue into the current game in the database
            game = Game.objects.filter(room_code=self.room_code)[0]
            game.current_clue = json_data['word']
            game.words_left = json_data['num']
            game.save()
            
            # then we send it out to all users
            message = json_data
            message['message_type'] = 'clue'
            async_to_sync(self.channel_layer.group_send)(self.room_group, message)
            
            # and we update the timer to start going
            self.updateTime(True)
            
        elif json_data['type'] == 'timer':
            # the timer has run out
            
            r = Game.objects.filter(room_code=self.room_code)[0]
            if not r.timer_ended:
                # we only do this if we haven't gotten the message before
                r.timer_ended
                
                # set the clue to nothing, set words left to 0, switch the team, and send out a message updating the team turn
                r.current_clue = ""
                r.words_left = 0
                r.team_turn = 1 if r.team_turn == 2 else 2
                r.save()
                async_to_sync(self.channel_layer.group_send)(self.room_group, {'type': 'turn', 'message_type': 'turn', 'team': r.team_turn})
                
                #update time so no current timer
                self.updateTime(False)
                
                
                #update the clue
                async_to_sync(self.channel_layer.group_send)(self.room_group, {'type': 'clue', 'message_type': 'clue', 'word': r.current_clue, 'num': r.words_left})
        else:
            message = json_data
            message['message_type'] = message['type']
            async_to_sync(self.channel_layer.group_send)(self.room_group, message)
            
    #this will be called to update the timer for users. ongoing is a Boolean, if true, game's lastClue will be set to right now and that time will be sent to all the computers.
    #if False, it will be set to datetime(2000,1,1,0,0,0) (no current clue) and a message saying that will be sent to the computers
    #
    def updateTime(self, ongoing):
        if ongoing:
            r = Game.objects.filter(room_code=self.room_code)[0]
            r.last_clue = datetime.now()
        else:
            r = Game.objects.filter(room_code=self.room_code)[0]
            r.last_clue = datetime.fromtimestamp(0, pytz.utc)
        
        r.timer_ended = False
        r.save()
        
        message = {
        'type': 'send_time',
        'message_type': 'send_time',
        'seconds_since_epoch': int(r.last_clue.timestamp())
        }
        
        async_to_sync(self.channel_layer.group_send)(self.room_group, message)
            
            
    # all of these functions basically have the same purpose:
    # they are called when an individual websocket is sent a message from the other websockets. They then forward the message to their specific computer.
    # more complex behavior is possible using these functions (and somewhat used in the "win" function) but for the most part a basic forwarding was sufficient for our program.
    def player(self, event):
        message = event.copy()
        del(message['type'])
        self.send(text_data = json.dumps(message))
 
    def clue(self, event):
        message = event.copy()
        del(message['type'])
        self.send(text_data = json.dumps(message))
    
    def turn(self, event):
        message = event.copy()
        del(message['type'])
        self.send(text_data = json.dumps(message))
        
    def button_press(self, event):
        message = event.copy()
        del(message['type'])
        #send message to socket
        self.send(text_data= json.dumps(message))

    def send_time(self, event):
        message = event.copy()
        del(message['type'])
        self.send(text_data= json.dumps(message))
    
    def win(self, event):
        p = Player.objects.filter(pk=self.player_id)[0]
        message = {
            'message_type': 'game_over',
            'Won?' : p.team == int(event['team'])
        }
        self.send(text_data= json.dumps(message))
        
