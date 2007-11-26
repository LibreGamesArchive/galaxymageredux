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

import pygame
from pygame.locals import *


class Director(object):
    def __init__(self, display, scene):
        self.display = display
        self.scene = scene
        self.clock = pygame.time.Clock()
        
    def resizeDisplay(self, width, height):
        self.display.resize(width, height)
        self.scene.rebuild()

    def action(self):
        self.scene.film()
        self.clock.tick()
        self.display.update()

        for event in pygame.event.get():
            if event.type is KEYDOWN:
                print self.clock.get_fps()
                if event.key == 27:
                    pygame.quit()
                    return False
            elif event.type is MOUSEBUTTONDOWN:
                self.scene.pick(event.pos)
        return True
