import pygame
from pygame.locals import *

import GIFImage
from make_safe_exec import test_safe_file


class Engine(object):
    def __init__(self, client):
        self.client = client

        self.scenario = 'main'
        self.am_master = False
        self.my_team = ""

        #TODO: when self.client.playing, we need to be running our own
        #update function, with our own App
        #bound to self.client.event_handler

    def talkToServer(self, command, args):
        self.client.avatar.callRemote('talkToGame', command, args)

    def youAreNowMaster(self, args):
        self.am_master = True
        self.game_master_submit_scenario_data()

    def game_master_submit_scenario_data(self):
        path = 'data/scenarios/%s/config.py'%self.scenario
        safe, why = test_safe_file(path)
        if safe:
            exec open(path, 'rU').read()
            self.talkToServer('getGameScenarioInfo', {'name':name, 'maxp':num_players, 'teams':teams})

    def getTalkFromServer(self, command, args):
        getattr(self, command)(args)
