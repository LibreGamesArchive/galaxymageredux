
import os
import ui_engine


global all_images, all_terrains, all_tiles_list, datadir
all_images = {}
all_terrains = {}
all_tiles_list = []


class Terrain(object):
    def __init__(self, name=None,
                 image_top=None, image_sides=(None, None, None, None),
                 color=(1,1,1,1), color_deviation=(0,0,0,0),
                 hitpoints=50, armor={}):

        self.name = name

        self.image_top = image_top
        self.image_sides = image_sides

        self.color = color
        self.color_deviation = color_deviation

        self.hitpoints = hitpoints

        self.armor = armor

        global all_terrains
        all_terrains[self.name] = self

def image(name=None, filename="None.png"):
    global all_images, datadir
    filename = os.path.join(datadir, *filename.split("/"))
    all_images[name] = ui_engine.load_image(filename)
    return None

def terrain_type(name=None,
                 image_top=None, image_sides=(None, None, None, None),
                 color=(1,1,1,1), color_deviation=(0,0,0,0),
                 hitpoints=50, armor={}):
    global all_image
    new = Terrain(name, all_images[image_top],
                  (all_images[image_sides[0]],
                   all_images[image_sides[1]],
                   all_images[image_sides[2]],
                   all_images[image_sides[3]]),
                  color, color_deviation,
                  hitpoints, armor)
    return None

def map_tile(x=0, y=0, bottom=0, height=5,
             terrain=None,
             tl_add=0, tr_add=0, bl_add=0, br_add=0):
    global all_terrains, all_tiles_list
    terrain = all_terrains[terrain]
    new = ui_engine.Tile((terrain.image_top,)+terrain.image_sides,
                         (x, y),
                         (tl_add, tr_add, bl_add, br_add),
                         bottom, height,
                         terrain.color,
                         terrain.color_deviation)

    all_tiles_list.append(new)

    return None

def load_map(filename):
    global datadir
    datadir = os.path.dirname(filename)
    a = open(filename, 'rU').read()
    exec a

    return all_images, all_terrains, all_tiles_list
