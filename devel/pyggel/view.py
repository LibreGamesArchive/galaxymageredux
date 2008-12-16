"""
pyggle.view
This library (PYGGEL) is licensed under the LGPL by Matthew Roe and PYGGEL contributors.

The view module contains functions and objects used to manipulate initiation, settings,
and changing of the screen window and OpenGL states.
"""

from OpenGL import error
oglError = error

from include import *

class _Screen(object):
    """A simple object to store screen settings."""
    def __init__(self):
        """Create the screen."""
        self.screen_size = (640, 480)
        self.rect = pygame.rect.Rect(0,0,*self.screen_size)
        self.fullscreen = False
        self.hwrender = True
        self.decorated = True
        self.lighting = True
        self.fog = True
        self.fog_color = (.5,.5,.5,.5)

        self.debug = True

        self.have_init = False

        self.clips = [(0,0,self.screen_size[0],self.screen_size[1])]
        glScissor(*self.clips[0])

    def set_size(self, size):
        """Set the screen size."""
        self.screen_size = size
        self.clips = [] #clear!
        self.clips.append((0,0,size[0],size[1]))
        self.rect = pygame.rect.Rect(0,0,*size)
        glScissor(*self.clips[0])

    def get_params(self):
        """Return the pygame window initiation parameters needed."""
        params = OPENGL|DOUBLEBUF
        if self.fullscreen:
            params = params|FULLSCREEN
        if self.hwrender:
            params = params|HWSURFACE
        if not self.decorated:
            params = params|NOFRAME
        return params

    def push_clip(self, new):
        """Push a new rendering clip onto the stack - used to limit rendering to a small area."""
        if self.clips: #we have an old one to compare to...
            a,b,c,d = new
            e,f,g,h = self.clips[-1] #last
            new = (max((a, e)), max((b, f)), min((c, g)), min((d, h)))
        self.clips.append(new)
        glScissor(*new)

    def pop_clip(self):
        """Pop the last clip off the stack."""
        if len(self.clips) == 1:
            return #don't pop the starting clip!
        self.clips.pop()
        glScissor(*self.clips[-1])

screen = _Screen()

def init(screen_size=None, use_psyco=True):
    """Initialize the display, OpenGL and whether to use psyco or not.
       screen_size must be the pixel dimensions of the display window
       use_psyco must be a boolean value indicating whether psyco should be used or not"""
    if screen_size:
        screen.set_size(screen_size)
    else:
        screen_size = screen.screen_size

    if use_psyco:
        try:
            import psyco
            psyco.background()
        except:
            pass

    pygame.init()
    build_screen()

    glEnable(GL_TEXTURE_2D)
    glFrontFace(GL_CW)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE);

    glEnable(GL_LIGHTING)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glEnable(GL_SCISSOR_TEST)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)

    glPointSize(10)

    clear_screen()
    set_fog_color()
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogf(GL_FOG_DENSITY, .35)
    glHint(GL_FOG_HINT, GL_NICEST)
    glFogf(GL_FOG_START, 10.0)
    glFogf(GL_FOG_END, 125.0)
    set_fog(True)
    glAlphaFunc(GL_GEQUAL, .5)
    set_background_color()

    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    screen.have_init = True

def set_background_color(rgb=(0,0,0)):
    """Set the background color (RGB 0-1) of the display."""
    glClearColor(*rgb+(0,))

def set_fullscreen(boolean):
    """Enable/Disable fullscreen mode."""
    screen.fullscreen = boolean
    build_screen()

def toggle_fullscreen():
    """Toggles fullscreen mode."""
    set_fullscreen(not screen.fullscreen)

def set_lighting(boolean):
    """Enable/Disable OpenGL lighting."""
    screen.lighting = boolean
    if boolean:
        glEnable(GL_LIGHTING)
    else:
        glDisable(GL_LIGHTING)

def toggle_lighting():
    """Toggle OpenGL lighting."""
    set_lighting(not screen.lighting)

def set_hardware_render(boolean):
    """Enable/Disable hardware rendering of screen."""
    screen.hwrender = boolean
    build_screen()

def toggle_hardware_render():
    """Toggle hardware rendering."""
    set_hardware_render(not screen.hwrender)

def set_decorated(boolean):
    """Enable/Disable window decorations (title bar, sides, etc.)"""
    screen.decorated = boolean
    build_screen()

def toggle_decorated():
    """Toggle window decorations."""
    set_decorated(not screen.decorated)

def set_fog_color(rgba=(.5,.5,.5,.5)):
    """Set the fog color (RGBA 0-1)"""
    glFogfv(GL_FOG_COLOR, rgba)
    screen.fog_color = rgba

def set_fog(boolean):
    """Enable/Disable fog."""
    screen.fog = boolean
    if boolean:
        glEnable(GL_FOG)
    else:
        glDisable(GL_FOG)

def toggle_fog():
    """Toggle fog."""
    set_fog(not screen.fog)

def set_fog_depth(min=10, max=125):
    """Set the min/max depth of fog."""
    glFogf(GL_FOG_START, min)
    glFogf(GL_FOG_END, max)

def set_debug(boolean):
    """Enable/Disable OpenGL debugging - specifically, this turns on/off calling of glGetError after every call."""
    screen.debug = boolean
    if boolean:
        oglError.ErrorChecker.registerChecker(None)
    else:
        oglError.ErrorChecker.registerChecker(lambda:None)

def toggle_debug():
    """Toggle OpenGL debugging."""
    set_debug(not screen.debug)

def build_screen():
    """Create the display window using the current set of screen parameters."""
    pygame.display.set_mode(screen.screen_size, screen.get_params())

def set2d():
    """Enable 2d rendering."""
    screen_size = screen.screen_size
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glOrtho(0, screen_size[0], screen_size[1], 0, -50, 50)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)

def set3d():
    """Enable 3d rendering."""
    screen_size = screen.screen_size
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0,0,*screen_size)
    gluPerspective(45, 1.0*screen_size[0]/screen_size[1], 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)

def refresh_screen():
    """Flip the screen buffer, displaying any changes since the last clear."""
    pygame.display.flip()

def clear_screen(scene=None):
    """Clear buffers."""
    glDisable(GL_SCISSOR_TEST)
    if scene and scene.graph.skybox:
        glClear(GL_DEPTH_BUFFER_BIT)
    else:
        glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
    glEnable(GL_SCISSOR_TEST)

def require_init():
    """Called if a function requires init to have been called - raises TypeError if not."""
    if not screen.have_init:
        raise TypeError, "pyggel.init must be called before this action can occur"
