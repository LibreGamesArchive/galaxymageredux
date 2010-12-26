import engine
from engine import *

import glob, os #might not be needed
import load_mod_file


#tile size is 1x1, no need to put that in for now though I hope

#gridToScreen - not needed, just render in 3d
#screenToGrid ^
#color_swap - we'll just colorize the texture on render
#ImageHandler - engines.helpers.TextureHandler


class MapEntity(object):
    def __init__(self, parent, renderable, colorize=(1,1,1,1), pos=(0,0), name="", anchor=None):
        self.parent = parent

        self.renderable = renderable #engine object to render, iamge only for now
        self.colorize = colorize

        self.pos = pos
        self.name = name

        self.anchor = anchor

        self.dead = False

        #no bound_to for now, unit entity class will be built for two entities...

        self.parent.entities.append(self)

    def kill(self):
        if self in self.parent.entities:
            self.parent.entities.remove(self)
            self.dead = True

    def get_tile_pos(self):
        return int(self.pos[0]), int(self.pos[1])

    def move(self, x, y):
        #TODO add handling of illegal/blocking tiles, or empty...
        x = self.pos[0] + x
        y = self.pos[1] + y
        if self.parent.map_grid:
            if x < 0:
                x = 0
            if x >= self.parent.map_bound_x: #add parent.map_bound_x
                x = self.parent.map_bound_x

            if y < 0:
                y = 0
            if y >= self.parent.map_bound_y:
                y = self.parent.map_bound_y

        self.pos = (x,y)

    def render(self):
        #TODO: convert self.pos to be correct based on anchor - which is render_pos from old gfx_engine!
        self.renderable.render(self.pos, self.colorize)


#MapHighlight - not needed, will just toggle and colorize highlighted tile!
#   Or outline it, whatever...
#   Outline would simply draw GL_LINES at edges of tiles
