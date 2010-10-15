
import include
from include import *

import display
import image
import texture

class Font2D(object):
    def __init__(self, name=None, tex_size=1024, def_size=32):
        self.name = name
        self.tex_size = tex_size
        self.def_size = def_size

        self._compile()

    def _compile(self):
        printable_chars = "abcdefghijklmnopqrstuvwxyz`1234567890-=[]\\;',./ "+'ABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+{}|:"<>?'

        texs = min((self.tex_size, display.get_max_texture_size()))

        num = len(printable_chars)
        rows = 10
        fsize = int(texs/rows*0.9)
        self.pygame_font = pygame.font.Font(self.name, fsize)
        ind = int(texs/rows)

        surf = pygame.Surface((texs, texs)).convert_alpha()
        surf.fill((0,0,0,0))

        char_map = {}

        on = 0
        for y in xrange(rows):
            for x in xrange(rows):
                if on < num:
                    char = printable_chars[on]
                    glyph = self.pygame_font.render(char, 1, (255,255,255))
                    surf.blit(glyph, (x*ind, y*ind))
                    char_map[char] = (x*ind, y*ind, glyph.get_width(), glyph.get_height())
                    on += 1

        self.tex = texture.Texture()
        self.tex._from_image(surf)
        glyph_map = {}

        for i in char_map:
            x,y,w,h = char_map[i]
            glyph_map[i] = image.Image2D(self.tex.get_region((x,y,x+w,y+h)))

        self.char_map = char_map
        self.glyph_map = glyph_map
        self.fsize = fsize

    def get_size(self, string, size=None):
        if size == None:
            size = self.def_size

        scale = size*1.0/self.fsize
        height = 0
        width = 0
        for char in string:
            glyph = self.glyph_map[char]
            height = max((height, glyph.texture.size[1]))
            width += glyph.texture.size[0]

        return width*scale, height*scale

    def get_height(self, size=None):
        if size == None:
            size = self.def_size

        scale = size*1.0/self.fsize
        height = self.pygame_font.get_height()

        return height * scale

    def render(self, string, pos, color=(1,1,1,1), size=None):
        if size == None:
            size = self.def_size
        scale = size*1.0/self.fsize
        glPushMatrix()
        glTranslatef(pos[0], pos[1], 0)
        glScalef(scale,scale,1)

        ind = 0
        for char in string:
            glyph = self.glyph_map[char]
            glyph.render((ind, 0), color)
            ind += glyph.texture.size[0]

        glPopMatrix()

    def make_size(self, size=None):
        if size == None:
            size = self.def_size
        return Font2Dcopy(self, size)

class Font2Dcopy(object):
    """References another font, but stores a dif def_size"""
    def __init__(self, other, def_size=None):
        self.other = other
        self.name = other.name
        self.tex_size = other.tex_size
        if def_size:
            self.def_size = def_size
        else:
            self.def_size = other.def_size

        self.tex = other.tex

        self.char_map = other.char_map
        self.glyph_map = other.glyph_map
        self.fsize = other.fsize

    def get_size(self, string, size=None):
        if size == None:
            size = self.def_size

        return self.other.get_size(string, size)

    def get_height(self, size=None):
        if size == None:
            size = self.def_size

        return self.other.get_height(size)

    def render(self, string, pos, color=(1,1,1,1), size=None):
        if size == None:
            size = self.def_size
        self.other.render(string, pos, color, size)

    def make_size(self, size=None):
        if size == None:
            size = self.def_size
        return Font2Dcopy(self.other, size)
