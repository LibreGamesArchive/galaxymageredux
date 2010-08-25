import pygame
from pygame.locals import *
import glob, os

import GIFImage
from make_safe_exec import test_safe_file

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
    def __init__(self, parent, image, pos=(0,0)):
        self.parent = parent
        self.image = image
        self.pos = (0,0)
        self.move(*pos)
        self.parent.entities.append(self)

    def kill(self):
        if self in self.parent.entities:
            self.parent.entities.remove(self)

    def get_real_pos(self):
        #TODO add camera handling here!
        cx,cy = self.parent.engine.camera.get_shift_pos()
        return int(self.pos[0]*tile_size[0]+cx), int(self.pos[1]*tile_size[1]+cy)

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

    def sort_entities(self, a, b):
        if a.pos[1] < b.pos[1]:
            return -1
        elif b.pos[1] < a.pos[1]:
            return 1
        elif a.pos[0] < b.pos[0]:
            return -1
        return 1

    def set_camera_pos(self, x, y):
        self.engine.camera.set_pos(x,y)
    def make_entity(self, image, pos):
        return MapEntity(self, image, pos)

    def load_map_file(self, path):
        ok = ['make_entity',#ok things for file to call
              'set_camera_pos']
        safe, why = test_safe_file(path, ok)
        if safe:
            engine = self
            tiles = {}
            map_grid = []
            exec open(path, 'rU').read()
            self.tiles = tiles
            self.map_grid = map_grid
        else:
            print why

    def render(self):
        yy = 0
        for y in self.map_grid:
            xx = 0
            for x in y:
                tname = x
                cx, cy = self.engine.camera.get_shift_pos()
                self.screen.blit(self.images.images[self.tiles[tname]], (xx*tile_size[0]+cx, yy*tile_size[1]+cy))
                xx += 1
            yy += 1

        self.entities.sort(self.sort_entities)
        for i in self.entities:
            i.render()

class Camera(object):
    def __init__(self):
        self.pos = (0,0)
        self.mapd = None

    def get_shift_pos(self):
        return 320-int(self.pos[0]*tile_size[0]), 240-int(self.pos[1]*tile_size[1])

    def move(self, x, y):
        x = self.pos[0] + x
        y = self.pos[1] + y
        if self.mapd:
            if x < 0:
                x = 0
            if x >= len(self.mapd.map_grid[0]):
                x = len(self.mapd.map_grid[0])

            if y < 0:
                y = 0
            if y >= len(self.mapd.map_grid):
                y = len(self.mapd.map_grid)

        self.pos = (x,y)

    def set_pos(self, x, y):
        x = x
        y = y
        if self.mapd:
            if x < 0:
                x = 0
            if x >= len(self.mapd.map_grid[0])-0.5:
                x = len(self.mapd.map_grid[0])-0.5

            if y < 0:
                y = 0
            if y >= len(self.mapd.map_grid)-0.5:
                y = len(self.mapd.map_grid)-0.5

        self.pos = (x,y)

class GFXEngine(object):
    def __init__(self, screen, scenario):
        self.screen = screen
        self.scenario = scenario
        self.load_images()
        self.camera = Camera()
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
        self.camera.mapd = self.mapd
