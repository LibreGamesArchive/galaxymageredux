#load dependancies
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math

import os
import time

try:
    import numpy
except:
    raise MissingModule("Numpy - you can get it from: http://sourceforge.net/projects/numpy/files/")

try:
    from OpenGL.GL.EXT.framebuffer_object import *
    FBO_AVAILABLE = True
except:
    FBO_AVAILABLE = False

try:
    from OpenGL.arrays import vbo
    VBO_AVAILABLE = bool(vbo.get_implementation())
except:
    VBO_AVAILABLE = False

try:
    from OpenGL.GL.EXT.texture_filter_anisotropic import *
    ANI_AVAILABLE = True
except:
    ANI_AVAILABLE = False

try:
    import Image as PIL
    TEX_ANI_AVAILABLE = True
except:
    TEX_ANI_AVAILABLE = False
    print "PIL not found - animated textures not supported!"
    print "\tYou can download PIL from: http://www.pythonware.com/products/pil/"

try:
    import psyco
    PSY_AVAILABLE = True
except:
    PSY_AVAILABLE = False

class MissingModule(Exception):
    pass

class MissingData(Exception):
    pass


#misc classes/functions
class PYGGEL_NOCHANGE(object):
    pass
def clamp(min, max, val):
    if val < min:
        val = min
    if val > max:
        val = max
    return val
def clamp_area(to, val):
    x1,y1,x2,y2 = val
    ox1,oy1,ox2,oy2 = to

    x1 = clamp(ox1, ox2, x1)
    x2 = clamp(ox1, ox2, x2)
    y1 = clamp(oy1, oy2, y1)
    y2 = clamp(oy1, oy2, y2)

    return (x1,y1,x2,y2)
