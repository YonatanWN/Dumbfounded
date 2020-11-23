"""Name: models.py
Purpose: Provides models to represent database entries for important data
Version: Added documentation, June 9th 2020
Authors:  Luke Patton
Dependecies: python, django"""

from django.db import models
from random import randrange
from game.words import random_word
from django.utils import timezone
import random
import pytz
from datetime import datetime
# each of these models inherits from django's Model base class. THey represent an entry in a database, but abstracted so it can be applied to a variety of databases

class Game(models.Model):
    # this model represents a specific "room" of the DumbFounded game. It holds information about the game state.
    
    #This function will generate a random room code that is 4 characters long, and this will be the default when creating a new room
    def random_room_code():
        code = ''
        for i in range(4):
            letters = ["F", "G", "H", "J", "K", "L", "Q", "R", "S", "V", "W", "X", "Y", "Z", "A", "E", "I", "O", "U"]
            code += letters[randrange(len(letters))]
        for game in Game.objects.all():
            #If any other room has this code, generate a new one
            if game.room_code==code:
                return random_room_code()
        return code
        
    def setup_default_grid(self, width=5, height=5, words_per_side=8):
        # side_counts is a variable that will count up how many tiles belong to each side so far, while side_maxes is the maximum number of tiles allowed to each side.
        side_counts = [0,0,0,0]
        
        
        side_maxes = [1, (width * height) - ((words_per_side * 2) + 2), words_per_side, words_per_side]
        
        if self.team_turn == 1:
            side_maxes[2] += 1
        else:
            side_maxes[3] += 1
        
        for x in range(width):
            for y in range(height):
                word = random_word()
                # keep randomizing word until we get one not on the list
                while self.boardposition_set.filter(word__startswith=word).count() != 0:
                    word = random_word()
                    
                side = random.randrange(4)
                
                #keep randomizing side until we get a side that isn't at its max
                
                while side_counts[side] + 1 > side_maxes[side]:
                    side = random.randrange(4)
                    
                side_counts[side] += 1
                
                self.boardposition_set.create(x=x, y=y, word=word,team=side - 1)
    # room_code is a unique code used to identify the room (and entered by the players to join the room)
    # we use random_room_code to generate a code by default
    room_code = models.CharField(max_length=4, default=random_room_code)
    
    # team turn represents which team's turn it is.
    team_turn = models.IntegerField()
    # current_clue and words_left together represent the clue and how many words are associated with it
    current_clue = models.CharField(default="", max_length=20)
    words_left = models.IntegerField(default=0)
    
    # last_clue holds the time when the last clue was put in (used for the timer)
    last_clue = models.DateTimeField(default=datetime.fromtimestamp(0, pytz.utc))
    
    # timer_ended is a boolean that represents whether the timer has ended yet
    timer_ended = models.BooleanField(default=True)


# board position (BP) is a model that holds information about one of the "cards" in a specific game
class BoardPosition(models.Model):
    # game is a foreign key that references a Game model (the game that the BP belongs to)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    
    # x and y hold the location of the BP
    x = models.IntegerField()
    y = models.IntegerField()
    
    # word holds the word that is on the card
    word = models.CharField(max_length=20)
    
    # we represent what team the board position belongs to with an integer--team. 0- no one, 1- team 1, 2- team 2, -1 - assassin
    team = models.IntegerField(default=0)
    
    # revealed is a boolean that stores whether the BP has been revealed
    revealed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.word

# player is a model that holds information about a specific player in a game
class Player(models.Model):
    # game is a foreign key that references a Game model (the game that the player belongs to)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    
    # name is the player's name
    name = models.CharField(max_length=20)
    
    # team is the team the player belongs to
    team = models.IntegerField(default=0)
    
    # captain is a boolean that stores whether the player is the team captain for their team
    captain = models.BooleanField(default=False)
    
    # avatar_num is an int that represents which avatar the player chose
    avatar_num = models.IntegerField(default=0)
    
    # room_alerted stores whether the player's room has been "alerted" that they joined (so they don't get alerted more than once)
    room_alerted = models.BooleanField(default=False)
    
    # connected is a boolean that holds whether the player is currently connected to the game
    # (so they can rejoin if they have left)
    connected = models.BooleanField(default=False)
    
    #assign should be called as soon as object is created. It randomly assigns the player to a team and determines whether they should be captain
    def assign(self):
        self.team = ((len(self.game.player_set.all()) - 1)% 2) + 1
        self.captain = (len(self.game.player_set.filter(team= self.team)) == 0)
        
    def __str__(self):
        return self.name

