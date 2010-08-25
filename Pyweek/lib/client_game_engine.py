import pygame
from pygame.locals import *

import GIFImage
from make_safe_exec import test_safe_file


class Engine(object):
    def __init__(self, client):
        self.client = client

        self.scenario = 'main'
        self.am_master = False
        self.game_name = ""
        self.my_team = ""
        self.player_name = self.client.username
        self.free_teams = []
        self.players = []
        self.max_players = 2

        #TODO: when self.client.playing, we need to be running our own
        #update function, with our own App
        #bound to self.client.event_handler

    def talkToServer(self, command, args):
        self.client.avatar.callRemote('talkToGame', command, args)

    def youAreNowMaster(self, args):
        self.am_master = True
        self.game_master_submit_scenario_data()
        self.update_player_gui()

    def kickedDueToTooManyPlayers(self, args):
        #TODO: handle kicked
        pass

    def kickedDueToScenario(self, args):
        #TODO: handle kicked
        pass

    def update_player_gui(self):
        self.client.game_room_lobby_num_players.text = 'players (%s/%s)'%(len(self.players), self.max_players)
        self.client.game_room_lobby_scenario.text = self.scenario
        self.client.game_room_lobby_game_name.text = self.game_name
        self.client.game_room_lobby_players.set_players(
            self, self.players, self.free_teams)

    def playerNamesTeams(self, args):
        self.players = args
        self.update_player_gui()

    def scenarioChanged(self, args):
        scen, team, max_players = args
        self.scenario = scen
        self.my_team = team
        self.max_players = max_players
        self.update_player_gui()

    def game_master_submit_scenario_data(self):
        path = 'data/scenarios/%s/config.py'%self.scenario
        safe, why = test_safe_file(path)
        if safe:
            exec open(path, 'rU').read()
            self.talkToServer('getGameScenarioInfo', {'name':name, 'maxp':num_players, 'teams':teams})

    def stillFreeTeamNames(self, args):
        self.free_teams = args
        self.update_player_gui()

    def masterKickPlayer(self, name):
        self.talkToServer('kickPlayer', name)

    def getTalkFromServer(self, command, args):
        getattr(self, command)(args)
