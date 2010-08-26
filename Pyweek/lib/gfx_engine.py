import pygame
from pygame.locals import *
import glob, os

import GIFImage
import load_mod_file

tile_size = (32,32)

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
        return (int(self.pos[0]*tile_size[0]*0.5 - self.pos[1]*tile_size[1]*0.5+cx),
                int(self.pos[1]*tile_size[1]*0.5 + self.pos[0]*tile_size[0]*0.5+cy))

    def get_my_tile(self):
        return int(self.pos[0]), int(self.pos[1])

    def move(self, x, y):
        x = self.pos[0] + x
        y = self.pos[1] + y
        if self.parent.map_grid:
            if x < 0:
                x = 0
            if x >= len(self.parent.map_grid[0])-0.5:
                x = len(self.parent.map_grid[0])-0.5

            if y < 0:
                y = 0
            if y >= len(self.parent.map_grid)-0.5:
                y = len(self.parent.map_grid)-0.5

        self.pos = (x,y)

    def render(self):
        image = self.parent.images.images[self.image]
        r = image.get_rect()
        r.midbottom = self.get_real_pos()
        try:
            image.render(self.parent.screen, r)
        except:
            self.parent.screen.blit(image, r)

class MapHandler(object):
    def __init__(self, engine):
        self.tiles = {}
        self.map_grid = []
        self.engine = engine
        self.screen = engine.screen
        self.images = engine.images
        self.entities = []

        self.tile_size = tile_size

    def sort_entities(self, a, b):
        if a.pos[1] < b.pos[1]:
            return -1
        elif b.pos[1] < a.pos[1]:
            return 1
        elif a.pos[0] < b.pos[0]:
            return -1
        return 1

    def make_entity(self, image, pos, name=''):
        return MapEntity(self, image, pos, name)

    def load_map_file(self, path):
        access = {"game":self.engine.client,
                  'gfx_engine':self.engine}
        succeed = load_mod_file.load(path, access)
        if succeed == False:
            self.engine.failed = True

    def render(self):
        yy = 0
        for y in self.map_grid:
            xx = 0
            for x in y:
                tname = x
                cx, cy = self.engine.camera.get_shift_pos()
                self.screen.blit(self.images.images[self.tiles[tname]],
                                 (xx*self.tile_size[0]/2-yy*self.tile_size[1]/2+cx,
                                  xx*self.tile_size[0]/2+yy*self.tile_size[1]/2+cy))
                xx += 1
            yy += 1

        self.entities.sort(self.sort_entities)
        for i in self.entities:
            i.render()

    def get_mouse_tile(self):
        mx, my = pygame.mouse.get_pos()
        cx, cy = self.engine.camera.get_shift_pos()
        xx = int((mx-cx)/self.tile_size[0]) if mx-cx else 0
        yy = int((my-cy)/self.tile_size[1]) if my-cy else 0
        return xx, yy

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
