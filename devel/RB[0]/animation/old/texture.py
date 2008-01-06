
import pygame
from OpenGL.GL import *

def get_dimensions(h, w):
    nh=16
    nw=16
    while nh < h:
        nh *= 2
    while nw < w:
        nw *= 2
    return nh, nw

class image:
    def __init__(self, filename=None, size="default"):
        self.image=glGenTextures(1)
        self.filename=filename
        self.size=size

        if self.filename:self.load_image()

    def load_image(self):
        textureSurface=pygame.image.load(self.filename)
        if self.size == "default":
            sh, sw = get_dimensions(*textureSurface.get_size())
        else:
            sh, sw = self.size, self.size
        textureSurface=pygame.transform.scale(textureSurface,(sh,sw))
        self.size = (sh, sw)

        textureData=pygame.image.tostring(textureSurface, "RGBA", 1)

        glBindTexture(GL_TEXTURE_2D, self.image)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(),
                     0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        return sh, sw

    def take_image(self, image):
        textureSurface=image
        if self.size == "default":
            sh, sw = get_dimensions(*textureSurface.get_size())
        else:
            sh, sw = self.size, self.size
        textureSurface=pygame.transform.scale(textureSurface,(sh,sw))

        textureData=pygame.image.tostring(textureSurface, "RGBA", 1)

        glBindTexture(GL_TEXTURE_2D, self.image)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(),
                     0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        return sh, sw

    def render_texture(self, size=1):
        glBindTexture(GL_TEXTURE_2D, self.image)

        glPushMatrix()
        glScale(size, size, size)
        glBegin(GL_POLYGON)
        glTexCoord2f(0,1);glVertex3f(-1,1,0)
        glTexCoord2f(1,1);glVertex3f(1,1,0)
        glTexCoord2f(1,0);glVertex3f(1,-1,0)
        glTexCoord2f(0,0);glVertex3f(-1,-1,0)
        glEnd()
        glPopMatrix()

    def render(self, size=1):
        self.render_texture(size)

    def render_image(self, size=1):
        glBindTexture(GL_TEXTURE_2D, self.image)

        dep_return=glGetBooleanv(GL_DEPTH_TEST)
        ble_return=glGetBooleanv(GL_BLEND)
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
        glPushMatrix()
        glScale(size, size, size)
        glBegin(GL_QUADS)
        glTexCoord2f(0,1);glVertex3f(-1,1,0)
        glTexCoord2f(1,1);glVertex3f(1,1,0)
        glTexCoord2f(1,0);glVertex3f(1,-1,0)
        glTexCoord2f(0,0);glVertex3f(-1,-1,0)
        glEnd()
        glPopMatrix()
        if dep_return:glEnable(GL_DEPTH_TEST)
        if not ble_return:glDisable(GL_BLEND)
        
