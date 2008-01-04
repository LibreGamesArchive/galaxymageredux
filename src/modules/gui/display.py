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


class Display(object):
    def __init__(self, width, height, isFullscreen=False):
        self.isFullscreen = isFullscreen
        pygame.init()
        self.resize(width, height)
        self.update()
    
    def resize(self, width, height):
        if height < 1:
            height = 1

        flags = OPENGL | DOUBLEBUF | HWSURFACE
        if self.isFullscreen:
            flags |= FULLSCREEN

        pygame.display.set_mode((width, height), flags)

    def update(self):
        pygame.display.flip()
