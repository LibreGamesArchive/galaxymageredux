import include
from include import *

import texture


#display controller
global __display
__display = None #can only have one
def get_display():
    global __display
    return __display
def set_display(display):
    global __display
    __display = display

def get_max_texture_size():
    return get_display().MAX_TEXTURE_SIZE

class Display(object):
    """This object controls initialization, modification, and destroying of the display"""
    def __init__(self):
        self.blank_texture = None
        self.MAX_TEXTURE_SIZE = 2**13 #max pygame can handle
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
        self.MAX_TEXTURE_SIZE = min((glGetIntegerv(GL_MAX_TEXTURE_SIZE),
                                     self.MAX_TEXTURE_SIZE))

        self.init_opengl()

        self.blank_texture = texture.Texture()
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
class Clip(object):
    def __init__(self, area, screen):
        self.area = area
        self.screen = screen
        if self.screen.clips:
            self.parent = self.screen.clips[-1]
        else:
            self.parent = None

    def get_clip(self):
        rx = 1.0 * self.screen.screen_size[0] / self.screen.screen_size_2d[0]
        ry = 1.0 * self.screen.screen_size[1] / self.screen.screen_size_2d[1]

        x, y, w, h = self.area
        if self.parent:
            ox, oy, ow, oh = self.parent.area
            x += ox
            y += oy
            if x + w > ox + ow:
                w = ox + ow - x
            if y + h > oy + oh:
                h = oy + oh - y

        return (int(x*rx), self.screen.screen_size[1]-int(y*ry)-int(h*ry), int(w*rx), int(h*ry))        

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

        self.clips = []
        self.push_clip((0,0,self.screen_size_2d[0], self.screen_size_2d[1]))

    def set_size(self, size, size2d):
        """Set the screen size."""
        if size:
            self.screen_size = size
        if size2d:
            self.screen_size_2d = size2d
            self.rect2d = pygame.rect.Rect(0,0,*size2d)

        size = self.screen_size
        self.clips = []
        self.push_clip((0,0,self.screen_size_2d[0], self.screen_size_2d[1]))
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
        new = Clip(new, self)
        self.clips.append(new)
        glScissor(*new.get_clip())

    def pop_clip(self):
        """Pop the last clip off the stack."""
        if len(self.clips) == 1:
            return #don't pop the starting clip!
        self.clips.pop()
        glScissor(*self.clips[-1].get_clip())

    def get_mouse_pos(self):
        """Return mouse pos in relation to the real screen size."""
        return pygame.mouse.get_pos()

    def get_mouse_pos2d(self):
        """Return mouse pos in relation to 2d screen size."""
        rx = 1.0 * self.screen_size_2d[0] / self.screen_size[0]
        ry = 1.0 * self.screen_size_2d[1] / self.screen_size[1]

        mx, my = pygame.mouse.get_pos()

        return int(mx*rx), int(my*ry)
