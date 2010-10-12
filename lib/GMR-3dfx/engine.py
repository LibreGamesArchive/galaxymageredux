
"""
Rendering engine for GalaxyMage Redux
Needs classes/functions for all rendering calls.
No where else should deal directly with OpenGL/Pygame gfx
"""

#load dependancies
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math

import os

try:
    import numpy
except:
    raise MissingModule("Numpy - you can get it from: http://sourceforge.net/projects/numpy/files/")

try:
    from OpenGL.GL.EXT.framebuffer_object import *
    FBO_AVAILABLE = True
except:
    FBO_AVAILABLE = False

try:
    from OpenGL.arrays import vbo
    VBO_AVAILABLE = bool(vbo.get_implementation())
except:
    VBO_AVAILABLE = False

try:
    from OpenGL.GL.EXT.texture_filter_anisotropic import *
    ANI_AVAILABLE = True
except:
    ANI_AVAILABLE = False

try:
    import GIFImage
    import time
    TEX_ANI_AVAILABLE = True
except:
    TEX_ANI_AVAILABLE = False
    print "PIL not found - animated textures not supported!"
    print "\tYou can download PIL from: http://www.pythonware.com/products/pil/"

try:
    import psyco
    PSY_AVAILABLE = True
except:
    PSY_AVAILABLE = False


global MAX_TEXTURE_SIZE
MAX_TEXTURE_SIZE = 2**13 #max pygame can handle


#error checking/disabling
from OpenGL import error as oglError
def quickCheckError(*args, **kwargs):
    return None
safeCheckError = oglError.ErrorChecker._registeredChecker

def set_debug(boolean):
    """Enable/Disable OpenGL debugging - specifically, this turns on/off calling of glGetError after every call."""
    if boolean:
        oglError.ErrorChecker._registeredChecker = safeCheckError
    else:
        oglError.ErrorChecker._registeredChecker = quickCheckError

class MissingModule(Exception):
    pass

class MissingData(Exception):
    pass


#misc classes/functions
class PYGGEL_NOCHANGE(object):
    pass
def clamp(min, max, val):
    if val < min:
        val = min
    if val > max:
        val = max
    return val
def clamp_area(to, val):
    x1,y1,x2,y2 = val
    ox1,oy1,ox2,oy2 = to

    x1 = clamp(ox1, ox2, x1)
    x2 = clamp(ox1, ox2, x2)
    y1 = clamp(oy1, oy2, y1)
    y2 = clamp(oy1, oy2, y2)

    return (x1,y1,x2,y2)


#display controller
global __display
__display = None #can only have one
def get_display():
    global __display
    return __display
def set_display(display):
    global __display
    __display = display

class Display(object):
    """This object controls initialization, modification, and destroying of the display"""
    def __init__(self):
        self.blank_texture = None
        self.screen = Screen()

    def setup(self, screen_size=None, screen_size_2d=None,
                 enable_psyco=True, icon_image=None,
                 fullscreen=False, hwrender=True,
                 caption="..."):
        if screen_size and not screen_size_2d:
            screen_size_2d = screen_size

        if enable_psyco and PSY_AVAILABLE:
            psyco.background()

        self.screen.set_size(screen_size, screen_size_2d)
        self.screen.fullscreen = fullscreen
        self.screen.hwrender = hwrender

        self.screen.icon = icon_image
        self.screen.caption = caption

    def build(self):
        if get_display():
            raise Exception("can only have one display active at one time!")
        set_display(self)
        pygame.init()

        self.set_icon()
        self.set_caption()
        self.set_screen()

        #this has to be set here...
        global MAX_TEXTURE_SIZE
        MAX_TEXTURE_SIZE = min((glGetIntegerv(GL_MAX_TEXTURE_SIZE),
                                MAX_TEXTURE_SIZE))

        self.init_opengl()

        self.blank_texture = BaseTexture()
        self.blank_texture.empty((2,2), (255,255,255,255))

    def clear(self):
        glDisable(GL_SCISSOR_TEST)
        glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
        glEnable(GL_SCISSOR_TEST)

    def refresh(self):
        pygame.display.flip()

    def destroy(self):
        #destroy display
        self.clear()
        glFlush()
        pygame.quit()
        set_display(None)
        self.blank_texture = None

    def init_opengl(self):
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glEnable(GL_SCISSOR_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)

        glPointSize(1)

        glAlphaFunc(GL_GEQUAL, .5)
        glClearColor(0,0,0,0)

        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glFrontFace(GL_CCW)
        glCullFace(GL_BACK)
        glEnable(GL_CULL_FACE)


    #Functions for applying updates/changes to attributes
    def set_caption(self, caption=PYGGEL_NOCHANGE):
        if caption is not PYGGEL_NOCHANGE:
            self.screen.caption = caption
        else:
            caption = self.screen.caption

        pygame.display.set_caption(caption)

    def set_icon(self, icon=PYGGEL_NOCHANGE):
        if icon is not PYGGEL_NOCHANGE:
            self.screen.icon = icon
        else:
            icon = self.screen.icon

        if type(icon) is type(""):
            pygame.display.set_icon(pygame.image.load(icon))
        elif icon:
            pygame.display.set_icon(icon)

    def set_screen(self, screen_size=PYGGEL_NOCHANGE,
                   screen_size_2d=PYGGEL_NOCHANGE,
                   fullscreen=PYGGEL_NOCHANGE,
                   hwrender=PYGGEL_NOCHANGE):
        if screen_size is not PYGGEL_NOCHANGE:
            if screen_size_2d is PYGGEL_NOCHANGE:
                screen_size_2d = screen_size
            self.screen.set_size(screen_size, screen_size_2d)

        if fullscreen is not PYGGEL_NOCHANGE:
            self.screen.fullscreen = fullscreen
        if hwrender is not PYGGEL_NOCHANGE:
            self.screen.hwrender = hwrender

        pygame.display.set_mode(self.screen.screen_size,
                                self.screen.get_params())

    def set_fog(self, color=PYGGEL_NOCHANGE,
                on=PYGGEL_NOCHANGE,
                depth=PYGGEL_NOCHANGE):
        if color is not PYGGEL_NOCHANGE:
            self.screen.fog_color = color
        if on is not PYGGEL_NOCHANGE:
            self.screen.fog = on
        if depth is not PYGGEL_NOCHANGE:
            min,max = depth

        glFogfv(GL_FOG_COLOR, self.screen.fog_color)
        if self.screen.fog:
            glEnable(GL_FOG)
        else:
            glDisable(GL_FOG)
        glFogf(GL_FOG_START, min)
        glFogf(GL_FOG_END, max)

    def set_lighting(self, on=PYGGEL_NOCHANGE):
        if on is not PYGGEL_NOCHANGE:
            self.screen.lighting = on

        if self.screen.lighting:
            glEnable(GL_LIGHTING)
        else:
            glDisable(GL_LIGHTING)

    def set_near_far_view(self, near=PYGGEL_NOCHANGE,
                          far=PYGGEL_NOCHANGE):
        if near is not PYGGEL_NOCHANGE:
            self.screen.view_near = near
        if far is not PYGGEL_NOCHANGE:
            self.screen.view_far = far

    def set_view_angle(self, angle=PYGGEL_NOCHANGE):
        if angle is not PYGGEL_NOCHANGE:
            self.screen.view_angle = angle

    def set_2d(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glOrtho(0, self.screen.screen_size[0],
                self.screen.screen_size[1],
                0, -50, 50)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)

        rx = 1.0 * self.screen.screen_size[0] / self.screen.screen_size_2d[0]
        ry = 1.0 * self.screen.screen_size[1] / self.screen.screen_size_2d[1]
        glScalef(rx, ry, 1)

    def set_3d(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glViewport(0,0,*self.screen.screen_size)
        gluPerspective(self.screen.view_angle,
                       1.0*self.screen.screen_size[0]/self.screen.screen_size[1],
                       self.screen.view_near, self.screen.view_far)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_DEPTH_TEST)


#screen/opengl/pygame params controller
class Screen(object):
    """A simple object to store screen settings."""
    def __init__(self):
        """Create the screen."""
        self.screen_size = (640, 480)
        self.screen_size_2d = (640, 480)
        self.rect = pygame.rect.Rect(0,0,*self.screen_size)
        self.rect2d = pygame.rect.Rect(0,0,*self.screen_size_2d)
        self.fullscreen = False
        self.hwrender = True
        self.caption = "GalaxyMage Redux"
        self.icon = None

        self.lighting = True
        self.fog = True
        self.fog_color = (.5,.5,.5,.5)

        self.view_angle = 45
        self.view_near = 0.1
        self.view_far = 100.0

        self.clear_color = (0,0,0,0)

        self.clips = [(0,0,self.screen_size[0],self.screen_size[1])]

    def set_size(self, size, size2d):
        """Set the screen size."""
        if size:
            self.screen_size = size
        if size2d:
            self.screen_size_2d = size2d
            self.rect2d = pygame.rect.Rect(0,0,*size2d)

        size = self.screen_size
        self.clips = [(0,0,size[0],size[1])]
        self.rect = pygame.rect.Rect(0,0,*size)

        return self.screen_size

    def get_params(self):
        """Return the pygame window initiation parameters needed."""
        params = OPENGL|DOUBLEBUF
        if self.fullscreen:
            params = params|FULLSCREEN
        if self.hwrender:
            params = params|HWSURFACE
        return params

    def push_clip(self, new):
        """Push a new rendering clip onto the stack - used to limit rendering to a small area."""
        if self.clips: #we have an old one to compare to...
            new = clamp_area(self.clips[-1], new)
        self.clips.append(new)
        glScissor(*new)

    def push_clip2d(self, new):
        """Convert a 2d pos/size rect into GL coords for clipping."""
        rx = 1.0 * self.screen_size[0] / self.screen_size_2d[0]
        ry = 1.0 * self.screen_size[1] / self.screen_size_2d[1]

        x, y, w, h = new

        self.push_clip((int(x*rx), self.screen_size[1]-int(y*ry)-int(h*ry), int(w*rx), int(h*ry)))

    def pop_clip(self):
        """Pop the last clip off the stack."""
        if len(self.clips) == 1:
            return #don't pop the starting clip!
        self.clips.pop()
        glScissor(*self.clips[-1])

    def get_mouse_pos(self):
        """Return mouse pos in relation to the real screen size."""
        return pygame.mouse.get_pos()

    def get_mouse_pos2d(self):
        """Return mouse pos in relation to 2d screen size."""
        rx = 1.0 * self.screen_size_2d[0] / self.screen_size[0]
        ry = 1.0 * self.screen_size_2d[1] / self.screen_size[1]

        mx, my = pygame.mouse.get_pos()

        return int(mx*rx), int(my*ry)


#### Basic data structures ####

class BaseTexture(object):
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

    def get_free_tex(self):
        if self.gl_tex is not None:
            return

        if BaseTexture._free:
            self.gl_tex = BaseTexture._free.pop()
        else:
            self.gl_tex = glGenTextures(1)

    def free_texture(self):
        if not self.gl_tex in BaseTexture._free:
            BaseTexture._free.append(self.gl_tex)
        self.size = (0,0)
        self.tex_data = None
        self.gl_tex = None

    def _get_next_biggest(self, x, y):
        """Get the next biggest power of two x and y sizes"""

        if x == y == 2:
            return x, y
        nw = 2
        nh = 2
        while nw < x and nw < MAX_TEXTURE_SIZE:
            nw *= 2
        while nh < y and nh < MAX_TEXTURE_SIZE:
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
        BaseTexture._bound = self.gl_tex
        glBindTexture(GL_TEXTURE_2D, self.gl_tex)
        tdata, w, h = self.tex_data

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, tdata)

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
        if self.gl_tex != BaseTexture._bound:
            glBindTexture(GL_TEXTURE_2D, self.gl_tex)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            BaseTexture._bound = self.gl_tex

        if self.repeat != BaseTexture._repeat:
            BaseTexture._repeat = self.repeat
            if self.repeat:
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
        if self.gl_tex != BaseTexture._bound:
            BaseTexture._bound = self.gl_tex
            glBindTexture(GL_TEXTURE_2D, self.gl_tex)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        if BaseTexture._repeat:
            BaseTexture._repeat = False
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

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

class DisplayList(object):
    """An object to compile and store an OpenGL display list"""
    def __init__(self):
        """Creat the list"""
        self.gl_list = glGenLists(1)

    def begin(self):
        """Begin recording to the list - anything rendered after this will be compiled into the list and not actually rendered"""
        glNewList(self.gl_list, GL_COMPILE)

    def end(self):
        """End recording"""
        glEndList()

    def render(self):
        """Render the display list"""
        glCallList(self.gl_list)

    def __del__(self):
        """Clear the display list data"""
        try:
            glDeleteLists(self.gl_list, 1)
        except:
            pass #already cleared!

class VertexArray(object):
    """An object to store and render an OpenGL vertex array of vertices, colors and texture coords"""
    def __init__(self, render_type=None, max_size=100):
        """Create the array
           render_type is the OpenGL constant used in rendering, ie GL_POLYGON, GL_TRINAGLES, etc.
           max_size is the size of the array"""
        if render_type is None:
            render_type = GL_QUADS
        self.render_type = render_type
        self.texture = BlankTexture()

        self.max_size = max_size

        self.verts = numpy.zeros((max_size, 3), "f")
        self.colors = numpy.zeros((max_size, 4), "f")
        self.texcs = numpy.zeros((max_size, 2), "f")
        self.norms = numpy.array([[0,1,0]]*max_size, "f")

    def render(self):
        """Render the array"""
        self.texture.bind()

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)

        glVertexPointerf(self.verts)
        glColorPointerf(self.colors)
        glTexCoordPointerf(self.texcs)
        glNormalPointerf(self.norms)

        glDrawArrays(self.render_type, 0, self.max_size)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)

    def reset_verts(self, data):
        self.verts = numpy.array(data, "f")
        self.max_size = len(data)

    def reset_colors(self, data):
        self.colors = numpy.array(data, "f")
        self.max_size = len(data)

    def reset_texcs(self, data):
        self.texcs = numpy.array(data, "f")
        self.max_size = len(data)

    def reset_norms(self, data):
        self.norms = numpy.array(data, "f")
        self.max_size = len(data)

    def update_verts(self, index, new):
        self.verts[index] = new

    def update_colors(self, index, new):
        self.colors[index] = new

    def update_texcs(self, index, new):
        self.texcs[index] = new

    def update_norms(self, index, new):
        self.norms[index] = new

    def resize(self, max_size):
        self.verts = numpy.resize(self.verts, (max_size, 3))
        self.colors = numpy.resize(self.colors, (max_size, 4))
        self.norms = numpy.resize(self.norms, (max_size, 3))
        self.texcs = numpy.resize(self.texcs, (max_size, 2))
        self.max_size = max_size

class VBOArray(object):
    def __init__(self, render_type=None, max_size=100, usage="static", cache_changes=False):
        """Create the array
           render_type is the OpenGL constant used in rendering, ie GL_POLYGON, GL_TRINAGLES, etc.
           max_size is the size of the array
           usage can be static, dynamic or stream (affecting render vs. modify speeds)
           cache_changes makes any changes between renderings be stored,
               and then only one modification is performed.
               NOTE: doing this actually modifies the entire buffer data, just efficiently
                     so this is only recommended if you are modifying a tremendous amount of points each frame!"""

        if not VBO_AVAILABLE:
            raise AttributeError("Vertex buffer objects not available!")

        self.usage = ("GL_"+usage+"_DRAW").upper()
        uses = {"GL_STATIC_DRAW":GL_STATIC_DRAW,
                "GL_DYNAMIC_DRAW":GL_DYNAMIC_DRAW,
                "GL_STREAM_DRAW":GL_STREAM_DRAW}
        self.usage_gl = uses[self.usage]

        self.cache_changes = cache_changes
        self._cached_cv = []
        self._cached_cc = []
        self._cached_ct = []
        self._cached_cn = []

        if render_type is None:
            render_type = GL_QUADS
        self.render_type = render_type
        self.texture = BlankTexture()

        self.max_size = max_size

        self.verts = vbo.VBO(numpy.zeros((max_size, 3), "f"), self.usage)
        self.colors = vbo.VBO(numpy.zeros((max_size, 4), "f"), self.usage)
        self.texcs = vbo.VBO(numpy.zeros((max_size, 2), "f"), self.usage)
        self.norms = vbo.VBO(numpy.array([[0,1,0]]*max_size, "f"), self.usage)

    def render(self):
        """Render the array"""
        if self.cache_changes:
            if self._cached_cv or self._cached_cc or self._cached_ct:
                for i in self._cached_cv:
                    self.verts.data[i[0]] = i[1]
                self.verts.bind()
                glBufferData(GL_ARRAY_BUFFER, self.verts.data, self.usage_gl)
                self._cached_cv = []

                for i in self._cached_cc:
                    self.colors.data[i[0]] = i[1]
                self.colors.bind()
                glBufferData(GL_ARRAY_BUFFER, self.colors.data, self.usage_gl)
                self._cached_cc = []

                for i in self._cached_ct:
                    self.texcs.data[i[0]] = i[1]
                self.texcs.bind()
                glBufferData(GL_ARRAY_BUFFER, self.texcs.data, self.usage_gl)
                self._cached_ct = []

                for i in self._cached_cn:
                    self.norms.data[i[0]] = i[1]
                self.norms.bind()
                glBufferData(GL_ARRAY_BUFFER, self.norms.data, self.usage_gl)
                self._cached_cn = []
        self.texture.bind()

        self.verts.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(self.verts)

        self.colors.bind()
        glEnableClientState(GL_COLOR_ARRAY)
        glColorPointerf(self.colors)

        self.texcs.bind()
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glTexCoordPointerf(self.texcs)

        self.norms.bind()
        glEnableClientState(GL_NORMAL_ARRAY)
        glNormalPointerf(self.norms)

        glDrawArrays(self.render_type, 0, self.max_size)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)

    def reset_verts(self, data):
        self.verts.set_array(numpy.array(data, "f"))
        self.max_size = len(data)

    def reset_colors(self, data):
        self.colors.set_array(numpy.array(data, "f"))
        self.max_size = len(data)

    def reset_texcs(self, data):
        self.texcs.set_array(numpy.array(data, "f"))
        self.max_size = len(data)

    def reset_norms(self, data):
        self.norms.set_array(numpy.array(data, "f"))
        self.max_size = len(data)

    def update_verts(self, index, new):
        if self.cache_changes:
            self._cached_cv.append([index, new])
        else:
            self.verts.bind()
            #index multiplier is
            #4*len(new) - so since verts have 3 points, we get 12
            glBufferSubData(GL_ARRAY_BUFFER, 12*index, numpy.array(new, "f"))
            self.verts.data[index] = new

    def update_colors(self, index, new):
        if self.cache_changes:
            self._cached_cc.append([index, new])
        else:
            self.colors.bind()
            glBufferSubData(GL_ARRAY_BUFFER, 16*index, numpy.array(new, "f"))
            self.colors.data[index] = new

    def update_texcs(self, index, new):
        if self.cache_changes:
            self._cached_ct.append([index, new])
        else:
            self.texcs.bind()
            glBufferSubData(GL_ARRAY_BUFFER, 8*index, numpy.array(new, "f"))
            self.texcs.data[index] = new

    def update_norms(self, index, new):
        if self.cache_changes:
            self._cached_cn.append([index, new])
        else:
            self.norms.bind()
            glBufferSubData(GL_ARRAY_BUFFER, 12*index, numpy.array(new, "f"))
            self.norms.data[index] = new

    def __del__(self):
        bufs = []
        for i in (self.verts, self.colors, self.texcs, self.norms):
            try:
                i.delete()
            except:
                pass #pyggel.quit() was called and we can no longer access the functions!

    def resize(self, max_size):
        self.max_size = max_size
        d = numpy.resize(self.verts.data, (max_size, 3))
        self.verts.set_array(d)

        d = numpy.resize(self.colors.data, (max_size, 4))
        self.colors.set_array(d)

        d = numpy.resize(self.texcs.data, (max_size, 2))
        self.texcs.set_array(d)

        d = numpy.resize(self.norms.data, (max_size, 3))
        self.norms.set_array(d)


#### Higher level data structures ####

class AnimatedTexture(object):
    def __init__(self):
        self.textures = []
        self.durations = []
        self.size = (0,0)
        self.size_mult = (1,1)
        self.area = (0,0,1,1)

        self.ptime = time.time()
        self.cur_frame = 0

    def _from_file(self, filename):
        self._from_image(GIFImage.GIFImage(filename))

    def _from_image(self, image):
        self._compile(image)

    def free_texture(self):
        for i in self.textures:
            i.free_texture()
        self.textures = []
        self.durations = []

    def _compile(self, image):
        self.textures = []
        self.durations = []
        for frame in image.frames:
            frame, dur = frame
            self.durations.append(dur)
            image = BaseTexture()
            image._from_image(frame)
            self.textures.append(image)
        self.size = self.textures[0].size
        self.size_mult = self.textures[0].size_mult
        self.area = self.textures[0].area

    def bind(self):
        if time.time() - self.ptime > self.durations[self.cur_frame]:
            self.cur_frame += 1
            if self.cur_frame >= len(self.textures):
                self.cur_frame = 0

            self.ptime = time.time()

        self.textures[self.cur_frame].bind()

    def bind_frame(self, frame):
        self.textures[frame].bind()

    def coord(self, x, y):
        return self.textures[0].coord(x,y)

    def get_region(self, area):
        return AnimatedTextureRegion(self, clamp_area(self.area, area))

class AnimatedTextureClone(TextureClone):
    def __init__(self, tex):
        TextureClone.__init__(self, tex)

        self.ptime = time.time()
        self.cur_frame = 0

    def bind(self):
        self.check_swap()
        self.tex.bind_frame(self.cur_frame)

    def check_swap(self):
        if time.time() - self.ptime > self.tex.durations[self.cur_frame]:
            self.cur_frame += 1
            if self.cur_frame >= len(self.tex.textures):
                self.cur_frame = 0

            self.ptime = time.time()

    def get_region(self, area):
        return self.tex.get_region(self, clamp_area(self.area, area))

class AnimatedTextureRegion(object):
    def __init__(self, tex, area):
        self.tex = tex

        self.textures = tex.textures
        self.durations = tex.durations
        self.area = area
        self.repeat = False

        x = self.area[2] - self.area[0]
        y = self.area[3] - self.area[1]
        self.size = x, y

        self.ptime = time.time()
        self.cur_frame = 0

    def bind(self):
        if time.time() - self.ptime > self.tex.durations[self.cur_frame]:
            self.cur_frame += 1
            if self.cur_frame >= len(self.tex.textures):
                self.cur_frame = 0

            self.ptime = time.time()

        gl_tex = self.textures[self.cur_frame].gl_tex
        if gl_tex != BaseTexture._bound:
            BaseTexture._bound = gl_tex
            glBindTexture(GL_TEXTURE_2D, gl_tex)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        if BaseTexture._repeat:
            BaseTexture._repeat = False
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

    def coord(self, x, y):
        x1,y1,x2,y2 = self.area

        x += x1
        y += y1

        x = clamp(x1,x2, x)
        y = clamp(y1,y2, y)
        return self.tex.coord(x,y)

    def get_region(self, area):
        return AnimatedTextureRegion(self, clamp_area(self.area, area))

def get_best_array_type(render_type=None, max_size=10,
                        opt=0):
    """This function returns the best possible array type for what you need.
       render_type is the OpenGL constant used in rendering, ie GL_POLYGON, GL_TRINAGLES, etc.
       max_size is the number of individual points in the array
       opt is how the array is optimized, starting at 0 for fast access to 5 for fast rendering
           5 also makes use of a cached VBO (if possible) - so it is very fast rendering and modifying
           *if* you are modifying a very large number of points - otherwise it is slower at modifying"""

    assert opt >= 0 and opt <= 5

    if not VBO_AVAILABLE:
        return VertexArray(render_type, max_size)

    if opt == 0:
        return VertexArray(render_type, max_size)
    elif opt == 1:
        return VBOArray(render_type, max_size, "stream")
    elif opt == 2:
        return VBOArray(render_type, max_size, "dynamic")
    elif opt == 3:
        return VBOArray(render_type, max_size, "static")
    else:
        return VBOArray(render_type, max_size, "static", True)


def load_texture(name):
    iname = name.split('.')[-1].lower()
    if iname in ('png', 'bmp', 'jpg'):
        short = os.path.split(name)[1]
        new = BaseTexture()
        new._from_file(name)
        return new
    if iname == 'gif':
        short = os.path.split(name)[1]
        new = AnimatedTexture()
        new._from_file(name)
        return new
    raise MissingData('No file "%s"'%name)

class TextureHandler(object):
    def __init__(self):
        self.textures = {}

    def load_dir(self, dire, replace=False):
        for i in os.listdir(dire):
            self.load_texture(i, replace)

    def load_texture(self, name, replace=False):
        if name.split('.')[-1].lower() in ('png', 'bmp', 'jpg', 'gif'):
            short = os.path.split(name)[1]
            if replace or (not short in self.textures):
                self.textures[short] = load_texture(name)

    def get_texture(self, name):
        if name in self.textures:
            tex = self.textures[name]
            if isinstance(tex, BaseTexture):
                return TextureClone(tex)
            else:
                return AnimatedTextureClone(tex)

    def free_textures(self):
        for i in self.textures.values():
            i.free_texture()
        self.textures = {}


#### Higher level drawing routines ####

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
        self.dlist = DisplayList()

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
        glColor4f(*Color(colorize).get_rgba1())
        self.texture.bind()
        self.dlist.render()
        glPopMatrix()

def load_image2D(name, area=None):
    return Image2D(load_texture(name), area)

class Font2D(object):
    def __init__(self, name=None, tex_size=1024):
        self.name = name
        self.tex_size = tex_size


        self._compile()

    def _compile(self):
        printable_chars = "abcdefghijklmnopqrstuvwxyz`1234567890-=[]\\;',./ "+'ABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+{}|:"<>?'

        texs = min((self.tex_size, MAX_TEXTURE_SIZE))

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

        self.tex = BaseTexture()
        self.tex._from_image(surf)
        glyph_map = {}

        for i in char_map:
            x,y,w,h = char_map[i]
            glyph_map[i] = Image2D(self.tex.get_region((x,y,x+w,y+h)))

        self.char_map = char_map
        self.glyph_map = glyph_map
        self.fsize = fsize

    def get_size(self, string, size=None):
        if size == None:
            size = self.fsize

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
            size = self.fsize

        scale = size*1.0/self.fsize
        height = self.pygame_font.get_height()

        return height * scale

    def render(self, string, pos, color=(1,1,1,1), size=None):
        if size == None:
            size = self.fsize
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

def draw_rect2d(area, color=(1,1,1,1), texture=None, tex_scale=True):
    area = pygame.Rect(area)

    if texture==None:
        texture = get_display().blank_texture

    if tex_scale:
        w = texture.size[0]
        h = texture.size[1]
    else:
        w = clamp(0, texture.size[0], area.width)
        h = clamp(0, texture.size[1], area.height)
    topleft = texture.coord(0, 0)
    topright = texture.coord(w,0)
    bottomleft = texture.coord(0,h)
    bottomright = texture.coord(w,h)
    texture.bind()

    glColor4f(*Color(color).get_rgba1())
    glBegin(GL_QUADS)
    glTexCoord2f(*topleft)
    glVertex3f(area.left, area.top, 0)
    glTexCoord2f(*bottomleft)
    glVertex3f(area.left, area.bottom, 0)
    glTexCoord2f(*bottomright)
    glVertex3f(area.right, area.bottom, 0)
    glTexCoord2f(*topright)
    glVertex3f(area.right, area.top, 0)
    glEnd()

def draw_lines2d(pairs, color=(1,1,1,1)):
    glColor4f(*Color(color).get_rgba1())
    glBegin(GL_LINES)
    for pair in pairs:
        glVertex3f(pair[0][0], pair[0][1], 0)
        glVertex3f(pair[1][0], pair[1][1], 0)
    glEnd()

class Color(object):
    def __init__(self, val, form="rgba1"):
        if isinstance(val, Color):
            self.r, self.g, self.b, self.a = val.r, val.g, val.b, val.a
        elif len(val) == 3:
            r,g,b = val
            if form == "rgba1":
                a = 1
            elif form == "rgba255":
                a = 255
            else:
                raise Exception("form must be 'rgba1' or 'rgba255'")
        else:
            r,g,b,a = val

        if form == "rgba255":
            r,g,b,a = map(self.convert_255_to_1, (r,g,b,a))

        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def convert_255_to_1(self, val):
        return val*1.0/255 if val else 0

    def get_rgb1(self):
        return self.r, self.g, self.b

    def get_rgb255(self):
        return map(int, (self.r*255, self.g*255, self.b*255))

    def get_rgba1(self):
        return self.r, self.g, self.b, self.a

    def get_rgba255(self):
        return map(int, (self.r*255, self.g*255, self.b*255, self.a*255))
