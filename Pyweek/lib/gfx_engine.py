import pygame
from pygame.locals import *
import glob, os
from math import floor

import GIFImage
import load_mod_file

tile_size = (64,32)

def GridToScreen(c, r, cx, cy):
    return cx + c*tile_size[0]*0.5 + r*tile_size[0]*0.5, \
           cy - c*tile_size[1]*0.5 + r*tile_size[1]*0.5 

def ScreenToGrid(mx, my, cx, cy):
    '''Returns Column, Row pair. May return points outside the grid_bounds '''
    return (mx-cx)/tile_size[0] - (my-cy)/tile_size[1], \
           (mx-cx)/tile_size[0] + (my-cy)/tile_size[1]

class ImageHandler(object):
    def __init__(self):
        self.images = {}

    def load_dir(self, dire):
        for i in glob.glob(dire+'*.gif'):
            short = os.path.split(i)[1]
            if not short in self.images:
                #already there
                self.images[short] = GIFImage.GIFImage(i)
        for i in glob.glob(dire+'*.png'):
            short = os.path.split(i)[1]
            if not short in self.images:
                #already there
                img = pygame.image.load(i).convert_alpha()
                self.images[short] = img

class MapEntity(object):
    def __init__(self, parent, image, pos=(0,0), name=''):
        self.parent = parent
        self.image = image
        self.pos = (0,0)
        self.move(*pos)
        self.parent.entities.append(self)
        self.name = name

    def kill(self):
        if self in self.parent.entities:
            self.parent.entities.remove(self)

    def get_real_pos(self):
        cx,cy = self.parent.engine.camera.get_shift_pos()
        tw,th = self.parent.tile_size
        sx, sy = self.pos
        return (cx + sx*tw*0.5 + sy*tw*0.5,
                cy - sx*th*0.5 + sy*th*0.5 + th)

    def get_my_tile(self):
        return int(self.pos[0]), int(self.pos[1])

    def move(self, x, y):
        x = self.pos[0] + x
        y = self.pos[1] + y
        if self.parent.map_grid:
            if x < 0:
                x = 0
            if x >= len(self.parent.map_grid[0]):
                x = len(self.parent.map_grid[0])

            if y < 0:
                y = 0
            if y >= len(self.parent.map_grid):
                y = len(self.parent.map_grid)

        self.pos = (x,y)

    def render(self):
        image = self.parent.images.images[self.image]
        r = image.get_rect()
        r.midbottom = self.get_real_pos()
        try:
            image.render(self.parent.screen, r)
        except:
            self.parent.screen.blit(image, r)

class MapHighlight(MapEntity):
    def __init__(self, parent, image, pos=(0,0)):
        self.parent = parent
        self.image = image
        self.pos = (0,0)
        self.move(*pos)
        self.parent.highlights.append(self)

    def kill(self):
        if self in self.parent.highlights:
            self.parent.highlights.remove(self)

class MapHandler(object):
    def __init__(self, engine):
        self.tiles = {}
        self.map_grid = []
        self.engine = engine
        self.screen = engine.screen
        self.images = engine.images
        self.entities = []

        self.highlights = []

        self.tile_size = tile_size

    def sort_entities(self, a, b):
        if a.pos[1] < b.pos[1]:
            return 1
        elif b.pos[1] < a.pos[1]:
            return -1
        elif a.pos[0] < b.pos[0]:
            return 1
        return -1

    def make_entity(self, image, pos, name=''):
        return MapEntity(self, image, pos, name)

    def load_map_file(self, path):
        access = {"game":self.engine.client,
                  'gfx_engine':self.engine}
        succeed = load_mod_file.load(path, access)
        if succeed == False:
            self.engine.failed = True

    def add_highlight(self, image, pos):
        return MapHighlight(self, image, pos)
    def clear_highlights(self):
        self.highlights = []

    def render(self):
        r = 0
        tw, th = self.tile_size
        for row in self.map_grid:
            c = 0
            for col in row:
                cx, cy = self.engine.camera.get_shift_pos()
                self.screen.blit(self.images.images[self.tiles[col]],
                                 (cx + c*tw*0.5 + r*tw*0.5,
                                  cy - c*th*0.5 + r*th*0.5))
                c += 1
            r += 1

        for i in self.highlights:
            i.render()

        self.entities.sort(self.sort_entities)
        for i in self.entities:
            i.render()

    def get_mouse_tile(self):
        mx, my = pygame.mouse.get_pos()
        cx, cy = self.engine.camera.get_shift_pos()
        tw = float(self.tile_size[0])
        th = float(self.tile_size[1])
        xx = int(floor((mx-cx)/tw - (my-cy-th*0.5)/th) ) if mx-cx else 0
        yy = int(floor((mx-cx)/tw + (my-cy-th*0.5)/th)) if my-cy else 0

        if xx >= 0 and xx < len(self.map_grid[0]) and\
           yy >= 0 and yy < len(self.map_grid):
            return xx, yy
        return None

    def get_entities_on_tile(self, x, y):
        n = []
        for i in self.entities:
            a, b = i.get_my_tile()
            if a==x and b==y:
                n.append(i)
        return n

class Camera(object):
    def __init__(self, engine):
        self.pos = (0,0)
        self.engine = engine

    def get_shift_pos(self):
        return (320-int(self.pos[0]*self.engine.mapd.tile_size[0]),
                240-int(self.pos[1]*self.engine.mapd.tile_size[1]))

    def move(self, x, y):
        x = self.pos[0] + x
        y = self.pos[1] + y
        if self.engine.mapd:
            if x < 0:
                x = 0
            if x >= len(self.engine.mapd.map_grid[0]):
                x = len(self.engine.mapd.map_grid[0])

            if y < 0:
                y = 0
            if y >= len(self.engine.mapd.map_grid):
                y = len(self.engine.mapd.map_grid)

        self.pos = (x,y)

    def set_pos(self, x, y):
        x = x
        y = y
        if self.engine.mapd:
            if x < 0:
                x = 0
            if x >= len(self.engine.mapd.map_grid[0])-0.5:
                x = len(self.engine.mapd.map_grid[0])-0.5

            if y < 0:
                y = 0
            if y >= len(self.engine.mapd.map_grid)-0.5:
                y = len(self.engine.mapd.map_grid)-0.5

        self.pos = (x,y)

class GFXEngine(object):
    def __init__(self, screen, scenario, client=None):
        self.screen = screen
        self.scenario = scenario
        self.client = client
        self.failed = False
        self.load_images()
        self.mapd = None
        self.camera = Camera(self)
        self.load_map()

    def load_images(self):
        self.images = ImageHandler()
        self.images.load_dir('data/scenarios/%s/images/'%self.scenario)
        self.images.load_dir('data/images/')

    def load_map(self):
        self.mapd = MapHandler(self)
        self.mapd.load_map_file('data/scenarios/%s/map.py'%self.scenario)

    def render(self):
        self.mapd.render()
