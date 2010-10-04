
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

        #this has to be set here...
        global MAX_TEXTURE_SIZE
        MAX_TEXTURE_SIZE = min((glGetIntegerv(GL_MAX_TEXTURE_SIZE),
                                MAX_TEXTURE_SIZE))

        self.set_icon()
        self.set_caption()
        self.set_screen()

    def clear(self):
        pass

    def refresh(self):
        pass

    def destroy(self):
        #destroy display
        pass

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

        self.cursor = None
        self.cursor_visible = True
        self.cursor_center = False

        self.have_init = False

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

        size = self._get_next_biggest(*image.get_size())
        maxs = max_tex_size()
        if max(size) > maxs:
            image = pygame.transform.scale(image, (maxs, maxs))
            size = maxs, maxs

        new = pygame.Surface((min((maxs, size[0])), min((maxs, size[1]))))
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
        Texture.bound = self.gl_tex
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
            image._from_image(image)
            self.textures.append(image)

    def bind(self):
        if time.time() - self.ptime > self.durations[self.cur_frame]:
            self.cur_frame += 1
            if self.cur_frame > len(self.textures):
                self.cur_frame = 0

            self.ptime = time.time()

        self.textures[self.cur_frame].bind()


class TextureClone(object):
    def __init__(self, tex):
        self.tex = tex

    def bind(self):
        self.tex.bind()

    def coord(self, x, y):
        return self.tex.coord(x,y)

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

        
