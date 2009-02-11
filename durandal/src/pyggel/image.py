"""
pyggle.image
This library (PYGGEL) is licensed under the LGPL by Matthew Roe and PYGGEL contributors.

The image module contains classes to load and render both 2d and 3d (billboarded) images.
"""

from include import *

import view, data, misc

class Image(object):
    """A 2d image object"""
    def __init__(self, filename, pos=(0,0),
                 rotation=(0,0,0), scale=1,
                 colorize=(1,1,1,1), dont_load=False):
        """Create the Image
           filename must be a filename to an image file, or a pygame.Surface object
           pos is the 2d position of the image
           rotation is the 3d rotation of the image
           scale is the scale factor for the image
           colorize is the color of the Image
           dont_load forces the Image not to load a filename and compile
               Deprecated - used to create an image from a surface instead of loading"""
        view.require_init()
        self.filename = filename

        self.pos = pos

        if not dont_load:
            if type(filename) is type(""):
                self._load_file()
            else:
                self.compile_from_surface(filename)
                self.filename = None

        self.to_be_blitted = []
        self.rotation = rotation
        self.scale = scale
        self.colorize = colorize
        self.visible = True

    def copy(self):
        """Return a copy of the image - sharing the same data.DisplayList"""
        new = Image(self.filename, self.pos, self.rotation, self.scale,
                    self.colorize, True)
        new._pimage = self._pimage
        new._pimage2 = self._pimage2
        new._image_size = self._image_size
        new._altered_image_size = self._altered_image_size
        new.rect = new._pimage.get_rect()
        new.to_be_blitted = list(self.to_be_blitted)
        new.display_list = self.display_list
        new.texture = self.texture
        new.offset = self.offset
        return new

    def _get_next_biggest(self, x, y):
        """Return next largest power of 2 size for an image"""
        nw = 16
        nh = 16
        while nw < x:
            nw *= 2
        while nh < y:
            nh *= 2
        return nw, nh

    def test_on_screen(self):
        """Return whether the image is onscreen or not"""
        r = pygame.rect.Rect(self.pos, self._image_size)
        return view.screen.rect.colliderect(r)

    def _load_file(self):
        """Load an image file"""
        self._pimage = pygame.image.load(self.filename)

        sx, sy = self._pimage.get_size()
        xx, xy = self._get_next_biggest(sx, sy)

        self._pimage2 = pygame.Surface((xx, xy)).convert_alpha()
        self._pimage2.fill((0,0,0,0))

        self._pimage2.blit(self._pimage, (0,0))

        self._pimage = self._pimage2.subsurface(0,0,sx,sy)

        self._image_size = (sx, sy)
        self._altered_image_size = (xx, xy)

        self._texturize(self._pimage2)
        self.rect = self._pimage.get_rect()
        self._compile()

    def compile_from_surface(self, surf):
        """Prepare surf to be stored in a Texture and DisplayList"""
        self._pimage = surf
        sx, sy = self._pimage.get_size()
        xx, xy = self._get_next_biggest(sx, sy)

        self._pimage2 = pygame.Surface((xx, xy)).convert_alpha()
        self._pimage2.fill((0,0,0,0))

        self._pimage2.blit(self._pimage, (0,0))

        self._pimage = self._pimage2.subsurface(0,0,sx,sy)

        self._image_size = (sx, sy)
        self._altered_image_size = (xx, xy)

        self.rect = self._pimage.get_rect()

        self._texturize(self._pimage2)
        self._compile()

    def _texturize(self, image):
        """Bind image to a data.Texture"""
        self.texture = data.Texture(image)

    def _compile(self):
        """Compile the Image into a data.DisplayList"""
        self.offset = self.get_width()/2, self.get_height()/2
        self.rect.center = self.offset[0] + self.pos[0], self.offset[1] + self.pos[1]

        self.display_list = data.DisplayList()
        self.display_list.begin()
        self.texture.bind()
        off = self.offset
        l = -off[0]
        r = off[0]
        t = -off[1]
        b = off[1]

        w = self.get_width()*1.0/self._altered_image_size[0]
        h = self.get_height()*1.0/self._altered_image_size[1]

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(l, t, 0)

        glTexCoord2f(w, 0)
        glVertex3f(r, t, 0)

        glTexCoord2f(w, h)
        glVertex3f(r, b, 0)

        glTexCoord2f(0, h)
        glVertex3f(l, b, 0)
        glEnd()

        self.display_list.end()

    def blit(self, other, pos):
        """Blit another image to this one at pos offset - ONLY allowing an image to blitted once
           other is another image.Image
           pos is the x,y offset of the blit"""
        self.remove_blit(other)
        self.to_be_blitted.append([other, pos])

    def blit_again(self, other, pos):
        """Same as blit, except you can blit the same image multiple times"""
        self.to_be_blitted.append([other, pos])

    def render(self, camera=None):
        """Render the image
           camera can be None or the camera the scene is using"""
        if not self.test_on_screen():
            return None

        ox, oy = self.offset
        h, w = self.get_size()

        pos = self.pos

        glPushMatrix()
        glTranslatef(pos[0]+ox, pos[1]+oy, 0)

        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)

        try:
            glScalef(self.scale[0], self.scale[1], 1)
        except:
            glScalef(self.scale, self.scale, 1)

        glColor(*self.colorize)
        self.display_list.render()
        glPopMatrix()
        if self.to_be_blitted:
            view.screen.push_clip((pos[0], view.screen.screen_size[1]-pos[1]-h,w,h))
            for i in self.to_be_blitted:
                x, y = i[1]
                x += pos[0]
                y += pos[1]
                o = i[0].pos
                i[0].pos = (x, y)
                i[0].render()
                i[0].pos = o
            view.screen.pop_clip()

    def get_width(self):
        """Return the width in pixels of the image"""
        return self._image_size[0]

    def get_height(self):
        """Return the height in pixels of the image"""
        return self._image_size[1]

    def get_size(self):
        """Return the width/height size of the image"""
        return self._image_size

    def get_rect(self):
        """Return a pygame.Rect of the image"""
        self.rect.center = self.offset[0] + self.pos[0], self.offset[1] + self.pos[1]
        return self.rect

    def clear_blits(self):
        """Remove all blits from the image"""
        self.to_be_blitted = []

    def remove_blit(self, image):
        """Remove all blits of image from the Image"""
        for i in self.to_be_blitted:
            if i[0] == image:
                self.to_be_blitted.remove(i)

    def sub_image(self, topleft, size):
        """Return a new Image object representing a smaller region of this Image."""
        image = self._pimage.subsurface(topleft, size)
        return Image(image, self.pos, self.rotation, self.scale, self.colorize)


class Image3D(Image):
    """A billboarded 3d image"""
    def __init__(self, filename, pos=(0,0,0),
                 rotation=(0,0,0), scale=1,
                 colorize=(1,1,1,1), dont_load=False):
        """Create the Image3D
           filename must be a filename to an image file, or a pygame.Surface object
           pos is the 3d position of the image
           rotation is the 3d rotation of the image
           scale is the scale factor for the image
           colorize is the color of the Image
           dont_load forces the Image not to load a filename and compile
               Deprecated - used to create an image from a surface instead of loading"""
        Image.__init__(self, filename, pos, rotation,
                       scale, colorize, dont_load)

    def get_dimensions(self):
        """Return a tuple of (1,1,1) signifying the 3d dimensions of teh image - used by the quad tree"""
        return 1, 1, 1

    def get_pos(self):
        """Return the position of the Image3D"""
        return self.pos

    def get_scale(self):
        """Return the scale of the object."""
        try: return self.scale[0], self.scale[1], self.scale[2]
        except: return self.scale, self.scale, self.scale

    def render(self, camera=None):
        """Render the Image3D
           camera can be None or the camera the scene is using to render from"""
        h, w = self.get_size()

        pos = self.pos

        glPushMatrix()
        glTranslatef(pos[0], pos[1], -pos[2])
        if camera:
            camera.set_facing_matrix()
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        try:
            glScalef(self.scale[0], self.scale[1], 1)
        except:
            glScalef(self.scale, self.scale, 1)
        glColor(*self.colorize)
        glDisable(GL_LIGHTING)
        self.display_list.render()
        if view.screen.lighting:
            glEnable(GL_LIGHTING)
        glPopMatrix()

    def blit(self, *args, **kwargs):
        print "Image3D does not support this function!"

    clear_blits = blit
    remove_blit = blit
    blit_again = blit
    test_on_screen = blit

    def copy(self):
        """Return a copy og the Image - sharing the same data.DisplayList"""
        new = Image3D(self.filename, self.pos, self.rotation, self.scale,
                      self.colorize, True)
        new._pimage = self._pimage
        new._pimage2 = self._pimage2
        new._image_size = self._image_size
        new._altered_image_size = self._altered_image_size
        new.rect = new._pimage.get_rect()
        new.display_list = self.display_list
        new.texture = self.texture
        new.offset = self.offset
        return new

    def _load_file(self):
        """Load an image file"""
        self._pimage = pygame.image.load(self.filename)

        sx, sy = self._pimage.get_size()
        xx, xy = self._get_next_biggest(sx, sy)

        self._pimage2 = pygame.Surface((xx, xy)).convert_alpha()
        self._pimage2.fill((0,0,0,0))

        self._pimage2.blit(self._pimage, (0,0))

        self._pimage = self._pimage2.subsurface(0,0,sx,sy)

        self._image_size = (sx, sy)
        self._altered_image_size = (xx, xy)

        self._texturize(self._pimage2)
        self._compile()
        self.rect = self._pimage.get_rect()

    def compile_from_surface(self, surf):
        """Prepare a pygame.Surface object for 3d rendering"""
        self._pimage = surf
        sx, sy = self._pimage.get_size()
        xx, xy = self._get_next_biggest(sx, sy)

        self._pimage2 = pygame.Surface((xx, xy)).convert_alpha()
        self._pimage2.fill((0,0,0,0))

        self._pimage2.blit(self._pimage, (0,0))

        self._pimage = self._pimage2.subsurface(0,0,sx,sy)

        self._image_size = (sx, sy)
        self._altered_image_size = (xx, xy)

        self._texturize(self._pimage2)
        self._compile()

    def _compile(self):
        """Compile the rendering data into a data.DisplayList"""
        self.offset = self.get_width()/2, self.get_height()/2

        self.display_list = data.DisplayList()
        self.display_list.begin()
        self.texture.bind()

        w = self.get_width()*1.0/self._altered_image_size[0]
        h = self.get_height()*1.0/self._altered_image_size[1]

        gw, gh = self.get_size()

        if gw < gh:
            uw = gw * 1.0 / gh
            uh = 1
        elif gh < gw:
            uw = 1
            uh = gh * 1.0 / gw
        else:
            uw = uh = 1

        glBegin(GL_QUADS)
        glTexCoord2f(0, h)
        glVertex3f(-uw, -uh, 0)

        glTexCoord2f(w, h)
        glVertex3f(uw, -uh, 0)

        glTexCoord2f(w, 0)
        glVertex3f(uw, uh, 0)

        glTexCoord2f(0, 0)
        glVertex3f(-uw, uh, 0)
        glEnd()

        self.display_list.end()

    def sub_image(self, topleft, size):
        """Return a new Image3D object representing a smaller region of this Image3D."""
        image = self._pimage.subsurface(topleft, size)
        return Image3D(image, self.pos, self.rotation, self.scale, self.colorize)
