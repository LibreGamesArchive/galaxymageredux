# LICENSE:
#
# Copyright (c) 2007 GalaxyMage Redux contributors.
#
# GalaxyMage Redux is free software; you can redistribute it and/or 
# modify it under the terms of version 2 of the GNU General Public 
# License, as published by the Free Software Foundation.
# 
# GalaxyMage Redux is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GalaxyMage Redux; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import os
from twisted.internet import reactor

import pygame
from pygame.locals import *

from rbgfx import map_loader
from rbgfx.gfx import *

from network.basic import Client

class OpenGLClient(Client):
    def __init__(self, host, port, user):
        Client.__init__(self, host, port, user) # base connects to server
        init()
        set_3d()
        self.clock = pygame.time.Clock()

        c = Camera()
        c.move((0, 0, 0))
        c.distance = 15
        c.rotate((45, 45, 0))
        self.cam = c

        l = Light((0,0,-15),
                  (1,1,1,1),
                  (1,1,1,1),
                  (1,1,1,1))

        self.images, self.terrains, self.tiles = map_loader.load_map(
                os.path.join("..", "data", "maps", "test_map.py"))

        self.units = [] # store all units by position here
        self.myunit = Sprite(pygame.image.load(
                os.path.join("..", "data", "images", "unit_example.png")), c)

    def update(self):
        """Called once the client has connected and provides the main loop for
        graphics rendering."""
        click = False
        self.clock.tick(30) # need spare cycles, thanks

        for event in pygame.event.get():
            if event.type == QUIT or \
                event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                reactor.stop() # disconnect
                return

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.cam.rotate((0, 90, 0))
                if event.key == K_RIGHT:
                    self.cam.rotate((0, -90, 0))

            if event.type == MOUSEBUTTONDOWN:
                click = True

        pick = select_tiles(self.tiles, pygame.mouse.get_pos())
        if pick:
            pick.old_color = pick.color
            pick.set_color((1, 0, 1, 1))
            if click:
                click = False
                # Request to move to this location..
                self.avatar.callRemote('requestMove', 0, pick.get_top())
                #print 'Picked: ', pick.get_top()

        self.cam.update()
        for i in self.tiles:
            i.render()
        for i in self.units:
            self.myunit.render(i)
        pygame.display.flip()
        
        if pick:
            pick.set_color(pick.old_color)
            del pick.old_color

        # set a callback to this function, so it loops indefinitely
        reactor.callLater(0, self.update)

    # Methods callable by the server
    def remote_serverMessage(self, message):
        print 'Got "', message, '" from server'

    def remote_updateUnits(self, units):
        """Allows the server to send a list of units for display."""
        self.units = units
        
user = 'user' + str(os.getpid())
client = OpenGLClient("localhost", 44444, user)
client.connect()
