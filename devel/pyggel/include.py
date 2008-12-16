"""
pyggle.include
This library (PYGGEL) is licensed under the LGPL by Matthew Roe and PYGGEL contributors.

The include module imports all necessary libraries,
as well as creates a blank, white texture for general use on non-textured objects.
"""

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy


from data import Texture
import view
x = view.require_init #bypass the textures not wanting to load before init, blank texture doesn't require it...
view.require_init = lambda: None
image = pygame.Surface((2,2))
image.fill((255,255,255,255))
blank_texture = Texture(image)
view.require_init = x
