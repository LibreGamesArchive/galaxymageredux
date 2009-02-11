"""
pyggle.font
This library (PYGGEL) is licensed under the LGPL by Matthew Roe and PYGGEL contributors.

The font module contains classes to display text images.
"""

from include import *
import image, view

class Font(object):
    """A font object used for rendering text to images"""
    def __init__(self, filename=None, fsize=32):
        """Create the font
           filename can be None or the filename of the font to load (TTF)
           fsize is the size of the font"""
        view.require_init()
        self.filename = filename
        self.fsize = fsize
        self.fontname = str(self.filename) + ":" + str(self.fsize)

        self._load_font()

    def _load_font(self):
        """Load the font"""
        self.pygame_font = pygame.font.Font(self.filename, self.fsize)

    def make_text_image(self, text="", color=(1,1,1,1)):
        """Create an image.Image object with the text rendered to it.
           text is the text to render
           color is the color of the text (0-1 RGBA)"""
        if "\n" in text:
            text = text.split("\n")
            n = []
            h = self.pygame_font.get_height()
            w = 0
            tot = 0
            for i in text:
                n.append(self.pygame_font.render(i, True, (255, 255, 255)))
                nw = n[-1].get_width()
                if nw > w:
                    w = nw
                tot += h
            new = pygame.Surface((w, tot)).convert_alpha()
            new.fill((0,0,0,0))
            tot = 0
            for i in n:
                new.blit(i, (0, tot*h))
                tot += 1
            return image.Image(new, colorize=color)
            
        else:
            return image.Image(self.pygame_font.render(text, True, (255,255,255)),
                               colorize=color)

    def make_text_image3D(self, text="", color=(1,1,1,1)):
        """Create an image.Image3D object with the text rendered to it.
           text is the text to render
           color is the color of the text (0-1 RGBA)"""
        if "\n" in text:
            text = text.split("\n")
            n = []
            h = self.pygame_font.get_height()
            w = 0
            tot = 0
            for i in text:
                n.append(self.pygame_font.render(i, True, (255, 255, 255)))
                nw = n[-1].get_width()
                if nw > w:
                    w = nw
                tot += h
            new = pygame.Surface((w, tot)).convert_alpha()
            new.fill((0,0,0,0))
            tot = 0
            for i in n:
                new.blit(i, (0, tot*h))
                tot += 1
            return image.Image3D(new, colorize=color)
        else:
            return image.Image3D(self.pygame_font.render(text, True, (255,255,255)),
                                 colorize=color)

class MEFontImage(object):
    """A font image that renders more slowly,
       but allows faster and more efficient changing of text"""
    def __init__(self, fontobj, text="", colorize=(1,1,1,1)):
        """Create the text
           fontobj is the MEFont object that created this text
           text is the text string to render
           colorize is the color (0-1 RGBA) of the text"""
        self.text = text
        self.fontobj = fontobj
        self.colorize = colorize
        self.pos = (0,0)
        self.rotation = (0,0,0)
        self.scale = 1
        self.visible = True

    def render(self, camera=None):
        """Render the object
           camera can be None or the camera object used in the scene to render this
               Only here to maintain compatability with other 2d gfx"""
        fo = self.fontobj
        glPushMatrix()
        a, b, c = self.rotation
        glRotatef(a, 1, 0, 0)
        glRotatef(b, 0, 1, 0)
        glRotatef(c, 0, 0, 1)
        try:
            glScalef(self.scale[0], self.scale[1], 1)
        except:
            glScalef(self.scale, self.scale, 1)

        if "\n" in self.text:
            atext = self.text.split("\n")
            height = 0
            for text in atext:
                indent = 0
                for c in text:
                    o = fo.glyphs[c]
                    o.colorize = self.colorize
                    x, y = self.pos
                    x += indent
                    y += height
                    o.pos = (x, y)
                    o.render(camera)
                    indent += o.get_width()
                height += self.fontobj.pygame_font.get_height()
        else:
            indent = 0
            for c in self.text:
                o = fo.glyphs[c]
                o.colorize = self.colorize
                x, y = self.pos
                x += indent
                o.pos = (x, y)
                o.render(camera)
                indent += o.get_width()
        glPopMatrix()

    def copy(self):
        """Copy the text image"""
        n = MEFontImage(self.fontobj, self.text, self.colorize)
        n.pos = self.pos
        n.rotation = self.rotation
        n.scale = self.scale
        n.visible = self.visible
        return n

    def get_width(self):
        """Return the max width of the text - in pixels"""
        fo = self.fontobj
        if "\n" in self.text:
            mx = 0
            for text in self.text.split("\n"):
                x = 0
                for c in text:
                    x += fo.glyphs[c].get_width()
                if x > mx:
                    mx = x
        else:
            mx = 0
            for c in self.text:
                mx += fo.glyphs[c].get_width()
        return mx

    def get_height(self):
        """return the max height of the text - in pixels"""
        fo = self.fontobj
        x = 0
        if "\n" in self.text:
            return len(self.text.split("\n")) * self.fontobj.pygame_font.get_height()
        return self.fontobj.pygame_font.get_height()

    def get_size(self):
        """Return the size of the text - in pixels"""
        return (self.get_width, self.get_height)

class MEFont(object):
    """A font the produces text images that render a little slower, but are much faster to change text"""
    def __init__(self, filename=None, fsize=32):
        """Create the font object
           filename can be None or the filename of the font to load (TTF)
           fsize is the size of the font"""
        view.require_init()
        self.filename = filename
        self.fsize = fsize

        self._load_font()

    def _load_font(self):
        """Load the font, and create glyphs"""
        self.pygame_font = pygame.font.Font(self.filename, self.fsize)

        L = {}
        for i in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`1234567890-=+_)(*&^%$#@!~[]\\;',./<>?:\"{}| ":
            L[i] = image.Image(self.pygame_font.render(i, True, (255,255,255)))

        self.glyphs = L

    def make_text_image(self, text="", color=(1,1,1,1)):
        """Return a MEFontImage that holds the text
           text is the text to render
           color = the color of the text (0-1 RGBA)"""
        return MEFontImage(self, text, color)
