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
from OpenGL.GL import *
from OpenGL.GLU import *

class Display(object):
    def __init__(self, width, height, isFullscreen=False):
        self.isFullscreen = isFullscreen
        self.color = (0.17, 0.17, 0.17, 0.17)
        self.resize(width, height)
        self.clear()
        self.flip()

        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_POLYGON_OFFSET_FILL)
        glEnable(GL_BLEND)
        glShadeModel(GL_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    def resize(self, width, height):
        if height == 1:
            height = 1

        flags = pygame.OPENGL | pygame.DOUBLEBUF
        if self.isFullscreen:
            flags |= pygame.FULLSCREEN

        pygame.display.set_mode([width, height], flags)

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(width)/float(height), 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
    def flip(self):
        pygame.display.flip()

    def clear(self):
        glClearColor(*self.color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
