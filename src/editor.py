# LICENSE:
#
# Copyright (c) 2007 Brandon Barnes and GalaxyMage Redux contributors.
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

from twisted.internet import reactor

import pygame
from pygame.locals import *

from gui.display import Display
from gui.scene import Scene

from network.basic import Client

import qgl

class OpenGLClient(Client):
    def __init__(self, host, port, user):
        Client.__init__(self, host, port, user)
        self.display = Display(800, 600)
        self.scene = Scene()
        self.clock = pygame.time.Clock()
        self.text = qgl.scene.state.Text("", "mono.ttf")
        self.group = qgl.scene.Group(self.text)
        self.group.translate = (-10, 0, -30)
        self.scene.addBackground(self.group)

    def resizeDisplay(self, width, height):
        self.display.resize(width, height)
        self.scene.rebuild()

    def update(self):
        self.scene.film()
        self.clock.tick()
        self.display.update()

        for event in pygame.event.get():
            if event.type is KEYDOWN:
                print self.clock.get_fps()
                if event.key == 27:
                    pygame.quit()
                    reactor.stop()
                    return
            elif event.type is MOUSEBUTTONDOWN:
                self.scene.pick(event.pos)
        
        reactor.callLater(0, self.update)

    # Methods callable by the server
    def remote_serverMessage(self, message):
        self.text.set_text(message)

        
user = raw_input("What is your name? ")
client = OpenGLClient("localhost", 44444, user)
client.connect()
