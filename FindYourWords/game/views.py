"""Name: views.py
Purpose: Handles views for our game, pulling templates and creating context
Version: Added documentation, June 9th 2020
Authors:  Luke Patton
Dependecies: python, django"""

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.template import loader
from game.words import random_word
from game.models import Game, Player
from django.urls import reverse
import random
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
def redirect_view(request):
    return HttpResponseRedirect(reverse('game:new'))


#gameroom is called when someone enters a gameroom. The details from the landing page are sent in "request" as part of a POST request.
# This information includes the player name, the avatar number they chose, the game pin of their game, and whether they are making or joining a game
def gameroom(request):
    post_request = request.POST.copy()
    
    
    #Get our inputs from the post request. If they weren't provided, set the variable to None.
    avatar = int(post_request['avatar']) if 'avatar' in post_request else None
    player_name = post_request['player_name'] if 'player_name' in post_request else None
    game_pin = post_request['gamepintxt'] if 'gamepintxt' in post_request else None
    mode = request.POST['mode'] if 'mode' in request.POST else 'make'
    
    
    #If no avatar was selected, but one of the dev names was entered, set their avatar to the appropriate avatar.
    if avatar == None:
        if player_name == 'Azra':
            avatar = 4
        elif player_name == 'Jackie':
            avatar = 5
        elif player_name == 'Luke':
            avatar = 6
        elif player_name == 'Yonatan':
            avatar = 7


    
    #if there is missing/incorrect information, we need to redirect back to the loading page. Get all the errors we need to return, then return the context
    error_messages = []
    
    if avatar == None:
        error_messages.append("Please select an avatar!")
    
    if player_name == None:
        error_messages.append("Please enter a name!")
        
    if game_pin == None:
        #if there is no game pin and the player is joining, tell them to enter a game pin.
        #if there is no game pin and the player is making a game, something went wrong, so tell them to try again (but don't bother if there are other errors anyway. Would seem confusing.
        if mode == 'join':
            error_messages.append("Please enter Game Pin!")
        elif error_messages == []:
            error_messages.append("Something went wrong. Please try again!")
    else:
        #if we do have a gamepin, and the mode is join, we have to see if the room exists.
        if mode == 'join' and len(Game.objects.filter(room_code=game_pin)) == 0:
            #if it doesn't, then tell them that
            error_messages.append("No room found with that pin!")
    
    # if we have errors, then get the landingpage again, load errors, and fill the info that was previously filled
    if len(error_messages) > 0:
        context = {"error_messages": error_messages}
        if player_name != None:
            context["player_name"] = player_name
        
        if avatar != None:
            context["avatar"] = avatar
            
        if game_pin != None:
            context["gamepintxt"] = game_pin
            
        context["mode"] = mode
        
        return render(request, 'game/creategame.html', context)
        
    
    
    
    #if mode is "make," then we are probably making a new game room.
    #It is possible that we would have mode "make" but a room already exists with the given pin.
    #Why? because the person who made the gameroom may have reloaded the page. this would send the same
    #post request, so we would act as though they are joining the game (try to add them as a player/rejoin as themself)
    game = None;
    if mode == 'make' and len(Game.objects.filter(room_code=game_pin)) == 0:
        #set up the game using the game pin we have from the frontend
        game = Game(team_turn = random.randrange(2) + 1, room_code=game_pin)
        if game != None:
            print("game is not none")
        else:
            print("game is none")
        game.save()
        
        #make the board
        game.setup_default_grid(width = int(post_request['boardsize']),height = int(post_request['boardsize']), words_per_side = int(post_request['wordsperside']))
        game.save()
        
        
        
    else:
        game = Game.objects.filter(room_code=game_pin)[0]
        
    game.save()
    
        
    #make a new player if there isn't currently a player with that name in the game. otherwise, check if the player is currently active; if they aren't then this player can take over their spot.
        
    if len(game.player_set.filter(name=player_name)) > 0:
        #someone exists with that name
        if game.player_set.filter(name=player_name)[0].connected and not mode == "make":
            #if they are currently connected, return back to landing page with appropriate error message.
            context = {"error_messages": ['Someone already has that name!']}
            if player_name != None:
                context["player_name"] = player_name
            
            if avatar != None:
                context["avatar"] = avatar
                
            if game_pin != None:
                context["gamepintxt"] = game_pin
                
            context["mode"] = mode
            
            return render(request, 'game/creategame.html', context)
        else:
            #they are not connected, so we can take over from them.
            player = game.player_set.filter(name=player_name)[0]
            
    else:
        #otherwise, no one exists with that name, so make a new player
            
        player = game.player_set.create(name=player_name, avatar_num=avatar)
        player.assign()
        
        player.save()
    
    #save our work on the game
    game.save()
       
    #now work on setup for the board and stuff
    rows = []
    y=0
    while len(game.boardposition_set.filter(y=y)) > 0:
        rows.append(game.boardposition_set.filter(y=y))
        y += 1
        
    
    
    #get all the player names on both teams
    team_1_players_query_set = game.player_set.filter(team=1)
    team_1_players = []
    for aplayer in team_1_players_query_set:
        team_1_players.append([aplayer.name, aplayer.avatar_num])
        
    team_2_players_query_set = game.player_set.filter(team=2)
    team_2_players = []
    for aplayer in team_2_players_query_set:
        team_2_players.append([aplayer.name, aplayer.avatar_num])
    
    
    template = loader.get_template('game/gameroom.html')
    
    #send info to template
    context = {
        'all_rows': rows,
        'room_code': game.room_code,
        'avatar_num': int(player.avatar_num),
        'players_name': player.name,
        'player_team': player.team,
        'is_captain': player.captain,
        'team_1_players': team_1_players,
        'team_2_players': team_2_players,
        'team_turn': game.team_turn,
        'pk': player.pk,
        'currentClue': game.current_clue,
        'wordsLeft': game.words_left
    }
    
    return HttpResponse(template.render(context,request))

# landing page loads our landing page by loading the template.
# it also sends a random room code for use in case the player is making a new game (it is auto filled in the gamepintxt box but disappears if they choose to join the game, handled in JS)
def landingpage(request):
    print("CHECK")
    template = loader.get_template('game/creategame.html')
    context = {'gamepintxt': Game.random_room_code}
    return HttpResponse(template.render(context, request))
