
import pyggel, os
from pyggel import *

from pyggel.misc import randfloat

def bind_range(val, range=(0,1)):
    if val < range[0]:
        val = range[0]
    if val > range[1]:
        val = range[1]
    return val

_images = {}
_terrain_types = {}
_tiles = []

def image(name, fn):
    if fn:
        _images[name] = pyggel.data.Texture("data/core/image/"+fn)
    else:
        _images[name] = None
def terrain_type(name="", image_top=None,
                 image_side=None,
                 color=(1,1,1,1),
                 color_deviation=(0,0,0,0)):
    _terrain_types[name] = (image_top, image_side,
                            color, color_deviation)
def map_tile(x=0, y=0, bottom=0, height=1,
             terrain="", tl_add=0, tr_add=0,
             bl_add=0, br_add=0):
    t_itop, t_iside, t_col, t_coldev = _terrain_types[terrain]
    if t_iside:
        t_iside = _images[t_iside]
    if t_itop:
        t_itop = _images[t_itop]
    pos = (x, bottom, -y)
    corners = (tl_add, tr_add, bl_add, br_add)
    r, g, b, a = t_col
    r2, g2, b2, a2 = t_coldev
    r += bind_range(randfloat(-r2, r2, 2))
    g += bind_range(randfloat(-g2, g2, 2))
    b += bind_range(randfloat(-b2, b2, 2))
    a += bind_range(randfloat(-a2, a2, 2))
    color = (r,g,b,a)
    side_texture = t_iside
    top_texture = t_itop
    _tiles.append(Tile(pos, height, corners, color,
                       side_texture, top_texture))

def parse_map(filename):
    if pyggel.misc.test_safe(filename, ["image", "terrain_type", "map_tile"])[0]:
        exec open(filename, "rU").read()
        return _tiles
    else:
        raise ImportWarning("Warning, map file <%s> is not safe!"%filename)

class Tile(object):
    def __init__(self, pos=(0,0,0), height=1,
                 corners=(0,0,0,0), colorize=(1,1,1,1),
                 side_texture=None, top_texture=None):

        self.pos = pos
        self.rotation = (0,0,0)
        self.visible = True
        self.pickable = True

        if not side_texture:
            side_texture = pyggel.data.BlankTexture()
        if not top_texture:
            top_texture = pyggel.data.BlankTexture()
        self.side_texture = side_texture
        self.top_texture = top_texture

        self.colorize = colorize
        self.corners = corners #topleft, topright, bottomleft, bottomright
        self.height = height

        self.display_list = pyggel.data.DisplayList()

        self._compile()

    def get_dimensions(self):
        return 1, max((self.height, self.height+max(self.corners))), 1

    def get_pos(self):
        return self.pos

    def _compile(self):
        self.display_list.begin()

        self.side_texture.bind()

        tl, tr, bl, br = self.corners
        mid = self.height
        tl += mid
        tr += mid
        bl += mid
        br += mid

        glBegin(GL_QUADS)
        #bottom first
        glNormal3f(*pyggel.math3d.calcTriNormal((-1,0,1),
                                              (1,0,-1),
                                              (1,0,1)))
        glTexCoord2f(0,0) #backleft
        glVertex3f(-1, 0, -1)
        glTexCoord2f(1,0) #backright
        glVertex3f(1, 0, -1)
        glTexCoord2f(1,1) #frontright
        glVertex3f(1, 0, 1)
        glTexCoord2f(0,1) #frontleft
        glVertex3f(-1, 0, 1)

        #left
        glNormal3f(*pyggel.math3d.calcTriNormal((-1,0,-1),
                                              (-1,1,-1),
                                              (-1,1,1)))
        glTexCoord2f(1,0) #backtop
        glVertex3f(-1, tl, -1)
        glTexCoord2f(0,0) #backbottom
        glVertex3f(-1, 0, -1)
        glTexCoord2f(0,1) #frontbottom
        glVertex3f(-1, 0, 1)
        glTexCoord2f(1,1) #fronttop
        glVertex3f(-1, bl, 1)

        #right
        glNormal3f(*pyggel.math3d.calcTriNormal((1,0,-1),
                                              (1,1,-1),
                                              (1,1,1)))
        glTexCoord2f(0,0) #backbottom
        glVertex3f(1, 0, -1)
        glTexCoord2f(1,0) #backtop
        glVertex3f(1, tr, -1)
        glTexCoord2f(1,1) #fronttop
        glVertex3f(1, br, 1)
        glTexCoord2f(0,1) #frontbottom
        glVertex3f(1, 0, 1)

        #front
        glNormal3f(*pyggel.math3d.calcTriNormal((-1,0,1),
                                              (-1,1,1),
                                              (1,1,1)))
        glTexCoord2f(1,0) #backtop
        glVertex3f(-1, bl, 1)
        glTexCoord2f(0,0) #backbottom
        glVertex3f(-1, 0, 1)
        glTexCoord2f(0,1) #frontbottom
        glVertex3f(1, 0, 1)
        glTexCoord2f(1,1) #fronttop
        glVertex3f(1, br, 1)

        #back
        glNormal3f(*pyggel.math3d.calcTriNormal((-1,0,-1),
                                              (-1,1,-1),
                                              (1,1,-1)))
        glTexCoord2f(0,0) #backbottom
        glVertex3f(-1, 0, -1)
        glTexCoord2f(1,0) #backtop
        glVertex3f(-1, tl, -1)
        glTexCoord2f(1,1) #fronttop
        glVertex3f(1, tr, -1)
        glTexCoord2f(0,1) #frontbottom
        glVertex3f(1, 0, -1)

        glEnd()

        self.top_texture.bind()
        glBegin(GL_TRIANGLES)
        #render left face first:
        glNormal3f(*pyggel.math3d.calcTriNormal((-1,tl,-1),
                                              (-1,bl,1),
                                              (0,mid,0)))
        glTexCoord2f(0, 1)
        glVertex3f(-1, tl, -1)
        glTexCoord2f(0, 0)
        glVertex3f(-1, bl, 1)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0, mid, 0)

        #render top face second:
        glNormal3f(*pyggel.math3d.calcTriNormal((1,tr,-1),
                                              (-1,tl,-1),
                                              (0,mid,0)))
        glTexCoord2f(0, 0)
        glVertex3f(1, tr, -1)
        glTexCoord2f(1, 0)
        glVertex3f(-1, tl, -1)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0, mid, 0)


        #render right face third:
        glNormal3f(*pyggel.math3d.calcTriNormal((1,br,1),
                                              (1,tr,-1),
                                              (0,mid,0)))
        glTexCoord2f(1, 0)
        glVertex3f(1, br, 1)
        glTexCoord2f(1, 1)
        glVertex3f(1, tr, -1)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0, mid, 0)

        #render bottom face last:
        glNormal3f(*pyggel.math3d.calcTriNormal((-1,bl,1),
                                              (1,br,1),
                                              (0,mid,0)))
        glTexCoord2f(0, 1)
        glVertex3f(-1, bl, 1)
        glTexCoord2f(1, 1)
        glVertex3f(1, br, 1)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0, mid, 0)

        glEnd()

        self.display_list.end()

    def render(self, camera=None):
        glPushMatrix()
        x, y, z = self.pos
        glTranslatef(x*2, y, -z*2)
        glColor4f(.5,.5,.5,1)
        self.display_list.render()
        glPopMatrix()

    def get_scale(self):
        return 1,1,1

class Unit(object):
    font = None
    def __init__(self, tile, pos=(0,0),
                 image=None, #change to/allow meshes later
                 colorize=(1,1,1,1)):
        if not self.font:
            self.font = pyggel.font.Font3D(size=20)
        self.image = image.copy()
        self.image.pos = pos[0], 0, pos[1]
        self.image.colorize = colorize
        self.pickable = True

        self.tile = tile

        self.text = self.font.make_text_image("HP: 20/20", color=(1,0,0,.5))

        self.hp = 20
        self.max_hp = 20
        self.visible = True

    def update_pos(self):
        x, y, z = self.tile.pos
        y = self.tile.pos[1] + self.tile.height+.5 #so we are correct height ;)
        self.image.pos = (x*2,y,z*2)

    def render(self, camera=None):
        self.update_pos()
        self.image.render(camera)
        self.text = self.font.make_text_image("HP: %s/%s"%(self.hp, self.max_hp), color=(1,0,0,1))
        self.text.pos = self.image.pos
        self.text.render(camera)
