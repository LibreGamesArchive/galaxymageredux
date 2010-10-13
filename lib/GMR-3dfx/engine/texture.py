import include
from include import *

import display

class Texture(object):
    _free = []
    _bound = None
    _repeat = False
    def __init__(self):

        self.gl_tex = None
        self.size = (0,0)
        self.size_mult = (1,1)
        self.area = (0,0,1,1)

        self.tex_data = None
        self.repeat = False

        self.mts = display.get_max_texture_size()

    def get_free_tex(self):
        if self.gl_tex is not None:
            return

        if Texture._free:
            self.gl_tex = Texture._free.pop()
        else:
            self.gl_tex = glGenTextures(1)

    def free_texture(self):
        if not self.gl_tex in Texture._free:
            Texture._free.append(self.gl_tex)
        self.size = (0,0)
        self.tex_data = None
        self.gl_tex = None

    def _get_next_biggest(self, x, y):
        """Get the next biggest power of two x and y sizes"""

        if x == y == 2:
            return x, y
        nw = 2
        nh = 2
        while nw < x and nw < self.mts:
            nw *= 2
        while nh < y and nh < self.mts:
            nh *= 2

        return nw, nh

    def _from_file(self, filename):
        """Loads file"""
        self._from_image(pygame.image.load(filename))

    def _from_image(self, image):
        """Creates a texture based on a raw Pygame Surface."""
        self._compile(image)

    def empty(self, size, color=(0,0,0,0)):
        image = pygame.Surface(size).convert_alpha()
        image.fill(color)
        self._from_image(image)

    def _compile(self, image):
        """Compiles image data into texture data"""
        self.get_free_tex()

        size = image.get_size()
        size2 = self._get_next_biggest(*size)
        if size != size2:
            x1,y1 = size
            x1 = max((size2[0], x1))
            y1 = max((size2[1], y1))
            if (x1,y1) != size:
                image = pygame.transform.scale(image, (x1, y1))

            new = pygame.Surface(size2).convert_alpha()
            new.fill((0,0,0,0))
            new.blit(image, (0,0))
        else:
            new = image

        tdata = pygame.image.tostring(new, "RGBA", 0)

        w1, h1 = image.get_size()
        w2, h2 = new.get_size()
        self.size = w1, h1
        self.area = (0,0,w1,h1)

        self.size_mult = (w1*1.0/w2,
                          h1*1.0/h2)

        self.tex_data = (tdata, w2, h2)

        self._from_tex_data()

    def _from_tex_data(self):
        Texture._bound = self.gl_tex
        glBindTexture(GL_TEXTURE_2D, self.gl_tex)
        tdata, w, h = self.tex_data

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, tdata)

        if self.repeat != Texture._repeat:
            Texture._repeat = self.repeat
            if self.repeat:
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_REPEAT)
            else:
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

        if ANI_AVAILABLE:
            try:
                glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAX_ANISOTROPY_EXT,glGetFloat(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT))
            except:
                pass

    def bind(self):
        """Binds the texture for usage"""
        self.bind_orepeat(self.repeat)

    def bind_orepeat(self, repeat):
        if self.gl_tex != Texture._bound:
            glBindTexture(GL_TEXTURE_2D, self.gl_tex)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            Texture._bound = self.gl_tex

        if repeat != Texture._repeat:
            Texture._repeat = repeat
            if repeat:
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_REPEAT)
            else:
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

    def coord(self, x, y):
        """Convert x,y coord to fit real tex"""
        x = 1.0*x / self.size[0] if x else 0
        y = 1.0*y / self.size[1] if y else 0
        return x*self.size_mult[0], y*self.size_mult[1]

    def get_region(self, area):
        return TextureRegion(self, clamp_area(self.area, area))

    def __del__(self):
        self.free_texture()

class TextureRegion(object):
    def __init__(self, tex, area):
        self.tex = tex
        self.gl_tex = self.tex.gl_tex
        self.area = area
        self.repeat = False

        x = self.area[2] - self.area[0]
        y = self.area[3] - self.area[1]
        self.size = x, y

    def bind(self):
        self.tex.bind_orepeat(False)

    def coord(self, x, y):
        x1,y1,x2,y2 = self.area

        x += x1
        y += y1

        x = clamp(x1,x2, x)
        y = clamp(y1,y2, y)
        return self.tex.coord(x,y)

    def get_region(self, area):
        return TextureRegion(self, clamp_area(self.area, area))


class TextureClone(object):
    def __init__(self, tex):
        self.tex = tex
        self.gl_tex = self.tex.gl_tex

        self.size = self.tex.size
        self.area = self.tex.area
        self.repeat = self.tex.repeat

    def bind(self):
        self.tex.bind()

    def coord(self, x, y):
        return self.tex.coord(x,y)

    def get_region(self, area):
        return self.tex.get_region(area)
