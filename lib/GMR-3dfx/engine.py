
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


#misc classes
class PYGGEL_NOCHANGE(object):
    pass


#display controller
class Display(object):
    """This object controls initialization, modification, and destroying of the display"""
    def __init__(self):
        self.screen = Screen()

    def setup(self, screen_size=None, screen_size_2d=None,
                 enable_psyco=True, icon_image=None,
                 fullscreen=False, hwrender=True,
                 caption="..."):
        if screen_size and screen_size_2d:
            screen_size_2d = screen_size

        if enable_psyco and PSY_AVAILABLE:
            psyco.background()

        self.screen.set_size(screen_size, screen_size_2d)
        self.screen.fullscreen = fullscreen
        self.screen.hwrender = hwrender

        self.screen.icon = icon_image
        self.screen.caption = caption

    def build(self):
        pygame.init()

        self.set_icon()
        self.set_caption()
        self.set_screen()

        #this has to be set here...
        global MAX_TEXTURE_SIZE
        MAX_TEXTURE_SIZE = min((glGetIntegerv(GL_MAX_TEXTURE_SIZE),
                                MAX_TEXTURE_SIZE))

        self.init_opengl()

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
            a,b,c,d = new
            e,f,g,h = self.clips[-1] #last
            new = (max((a, e)), max((b, f)), min((c, g)), min((d, h)))
        self.clips.append(new)
        glScissor(*new)

    def push_clip2d(self, pos, size):
        """Convert a 2d pos/size rect into GL coords for clipping."""
        rx = 1.0 * self.screen_size[0] / self.screen_size_2d[0]
        ry = 1.0 * self.screen_size[1] / self.screen_size_2d[1]

        x, y = pos
        w, h = size

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


#### Basic 2d data structures ####

class BaseTexture(object):
    _free = []
    def __init__(self):

        self.gl_tex = None
        self.size = (0,0)
        self.size_mult = (1,1)

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

    def _compile(self, image):
        """Compiles image data into texture data"""
        self.get_free_tex()

        size = image.get_size()
        size2 = self._get_next_biggest(*size)
        x1,y1 = size
        if size2[0] < x1:
            x1 = size2[0]
        if size2[1] < y1:
            y1 = size2[1]
        if (x1,y1) != size:
            size = (x1,y1)
            image = pygame.transform.scale(image, size)

        new = pygame.Surface(size2)
        new.blit(image, (0,0))

        tdata = pygame.image.tostring(new, "RGBA", 0)

        w1, h1 = image.get_size()
        w2, h2 = new.get_size()
        self.size = w1, h1

        self.size_mult = (w1*1.0/w2,
                          h1*1.0/h2)

        self.tex_data = (tdata, w2, h2)

        self._from_tex_data()

    def _from_tex_data(self):
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
        glBindTexture(GL_TEXTURE_2D, self.gl_tex)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

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
        return x*self.size_mult[0], y*self.size_mult[1]

class AnimatedTexture(object):
    def __init__(self):
        self.textures = []
        self.durations = []
        self.size = (0,0)
        self.size_mult = (1,1)

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


class TextureClone(object):
    def __init__(self, tex):
        self.tex = tex

        self.size = self.tex.size
        self.size_mult = self.tex.size_mult

    def bind(self):
        self.tex.bind()

    def coord(self, x, y):
        return self.tex.coord(x,y)

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

class TextureHandler(object):
    def __init__(self):
        self.textures = {}

    def load_dir(self, dire):
        for i in os.listdir(dire):
            ii = i.split('.')[-1]
            if ii.lower() in ('png', 'bmp', 'jpg'):
                short = os.path.split(i)[1]
                if not short in self.textures:
                    new = BaseTexture()
                    new._from_file(i)
                    self.textures[short] = new
            if ii.lower() == 'gif':
                short = os.path.split(i)[1]
                if not short in self.textures:
                    new = AnimatedTexture()
                    new._from_file(i)
                    self.textures[short] = new

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


#### Higher level drawing routines ####

class Image2D(object):
    def __init__(self, texture, area=None, dlist=None):
        self.texture = texture
        if area == None:
            area = 0,0,self.texture.size[0], self.texture.size[1]

        a = float(area[0]) / self.texture.size[0] if area[0] else 0
        b = float(area[1]) / self.texture.size[1] if area[1] else 0
        c = float(area[2]) / self.texture.size[0] if area[2] else 0
        d = float(area[3]) / self.texture.size[1] if area[3] else 0
        self.area = a,b,c,d

        self.dlist = dlist
        if not dlist:
            self._compile()

    def _compile(self):
        #Maybe changeme - just using display lists for images atm
        #they are lighter code-wise
        self.dlist = DisplayList()

        topleft = self.texture.coord(self.area[0],
                                     self.area[1])
        topright = self.texture.coord(self.area[2],
                                      self.area[1])
        bottomleft = self.texture.coord(self.area[0],
                                        self.area[3])
        bottomright = self.texture.coord(self.area[1],
                                         self.area[3])

        w,h = self.texture.size

        #render
        self.dlist.begin()

        self.texture.bind()
        glColor4f(1,1,1,1)
        glBegin(GL_QUADS)
##        glTexCoord2f(*topleft)
##        glVertex3f(0,0,0)
##        glTexCoord2f(*bottomleft)
##        glVertex3f(0,h,0)
##        glTexCoord2f(*bottomright)
##        glVertex3f(w,h,0)
##        glTexCoord2f(*topright)
##        glVertex3f(w,0,0)
        glTexCoord2f(0,0)
        glVertex3f(0,0,0)
        glTexCoord2f(0,1)
        glVertex3f(0,20,0)
        glTexCoord2f(1,1)
        glVertex3f(20,20,0)
        glTexCoord2f(1,0)
        glVertex3f(20,0,0)
        glEnd()

        self.dlist.end()

    def get_rect(self):
        return pygame.Rect((0,0), self.texture.size)

    def sub_image(self, area):
        x,y,w,h = area
        x+=self.area[0]
        y+=self.area[1]
        w = min(self.area[2], x+w)
        h = min(self.area[3], y+h)
        return Image(self.texture, (x,y,w,h))

    def copy(self):
        return Image(self.texture, self.area)

    def render(self, pos):
        glPushMatrix()
        glTranslatef(pos[0], pos[1], 0)
        self.dlist.render()
        glPopMatrix()
