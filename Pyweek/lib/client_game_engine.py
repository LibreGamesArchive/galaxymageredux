import pygame
from pygame.locals import *


class Engine(object):
    def __init__(self, avatar):
        self.avatar = avatar

        self.scenario = 'main'
        self.am_master = False
        self.my_team = ""

    def talkToServer(self, command, args):
        self.avatar.callRemote('talkToGame', command, args)
