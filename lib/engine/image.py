import storage

import include
from include import *

import misc

class Image2D(object):
    def __init__(self, texture, area=None, dlist=None):
        if area == None:
            self.texture = texture
        else:
            self.texture = texture.get_region(area)

        self.dlist = dlist
        if not dlist:
            self._compile()

    def _compile(self):
        #Maybe changeme - just using display lists for images atm
        #they are lighter code-wise
        self.dlist = storage.DisplayList()

        w,h = self.texture.size
        topleft = self.texture.coord(0, 0)
        topright = self.texture.coord(w,0)
        bottomleft = self.texture.coord(0,h)
        bottomright = self.texture.coord(w,h)

        #render
        self.dlist.begin()
        glBegin(GL_QUADS)
        glTexCoord2f(*topleft)
        glVertex3f(0,0,0)
        glTexCoord2f(*bottomleft)
        glVertex3f(0,h,0)
        glTexCoord2f(*bottomright)
        glVertex3f(w,h,0)
        glTexCoord2f(*topright)
        glVertex3f(w,0,0)
        glEnd()

        self.dlist.end()

    def get_rect(self):
        return pygame.Rect((0,0), self.texture.size)

    def copy(self, area=None):
        if area:
            tex = self.texture.get_region(area)
        else:
            tex = self.texture
        return Image2D(tex)

    def clone(self):
        """Reference copy"""
        return Image2D(self.texture, None, self.dlist)

    def render(self, pos, colorize=(1,1,1,1)):
        glPushMatrix()
        glTranslatef(pos[0], pos[1], 0)
        glColor4f(*misc.Color(colorize).get_rgba1())
        self.texture.bind()
        self.dlist.render()
        glPopMatrix()
