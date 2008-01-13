
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

def init(ScreenSize=(640, 480)):
    """creates a screen, enables required OpenGL rendering controls, and sets up the viewport"""

    pygame.init()

    pygame.display.set_mode(ScreenSize, OPENGL|DOUBLEBUF)#|FULLSCREEN)
        
    glEnable(GL_TEXTURE_2D)
    glFrontFace(GL_CCW)
    glEnable(GL_COLOR_MATERIAL)

    glEnable(GL_LIGHTING)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    glClearColor(1,1,1,1)

    set3d(ScreenSize)

    return None

def set2d(ScreenSize=(640, 480)):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, ScreenSize[0],
            0, ScreenSize[1],
            -1000, 1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    return None

def set3d(ScreenSize=(640, 480)):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0*ScreenSize[0]/ScreenSize[1],
                   0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    return None

def clear_screen():
    glClear(GL_DEPTH_BUFFER_BIT|GL_COLOR_BUFFER_BIT)
    return None

class Camera(object):
    def __init__(self, position=(0, 0, 0),
                 angle=(0, 0, 0),
                 distance=15):
        """This is a generic camera class.
           It is used to keep track of and move the position,
               angle and distance of the OpenGL camera.
           While there can be any number of Camera's active at one time,
               it should be noted that they are all technically in control of the
               <i>same</i> camera, and are just different settings.

           position is a list or tuple of len 3,
               it specifies the position that the camera is looking at.

           angle is a list or tuple of len 3,
               it specifies the angle the camera is turned to.

           distance is how far back the camera is from position."""

        self.position = position
        self.angle = angle
        self.distance = distance

        self.dirty = False

    def __check_values(self):
        """This method checks to make sure he angle of the camera is correct."""
        self.angle = list(self.angle)
        for i in range(len(self.angle)):
            while self.angle[i] > 360:
                self.angle[i] -= 360
            while self.angle[i] < 0:
                self.angle[i] += 360

        return None

    def rotate(self, angle=(0, 0, 0)):
        x, y, z = self.angle
        x += angle[0]
        y += angle[1]
        z += angle[2]

        self.angle = (x, y, z)
        return None

    def move(self, direction=(0, 0, 0)):
        x, y, z = self.position
        x += direction[0]
        y += direction[1]
        z += direction[2]

        self.position = (x, y, z)
        return None

    def update(self):
        """This method rotates, moves and then zooms the camera."""
        self.__check_values()
        if self.dirty:
            glPopMatrix()
            self.dirty = False

        glPushMatrix()

        glTranslatef(0, 0, -self.distance)

        glRotatef(self.angle[0], 1, 0, 0)
        glRotatef(self.angle[1], 0, 1, 0)
        glRotatef(self.angle[2], 0, 0, 1)

        glTranslatef(*self.position)

        self.dirty = True

        return None


class Light(object):
    num_lights=0
    def __init__(self, position=(0, 0, 0), specular=(0, 0, 0, 0),
                 ambient=(0, 0, 0, 0), diffuse=(0, 0, 0, 0),
                 shininess=50, directional=1):
        """This is a container class for a glLight.
           There should at most be 8 lights at one time.
           Each light is independant of the others, so any changes to
               will not affect the others.

           position is a list or tuple of len 3,
               it specifies the lights position in 3d space.

           specular is a list or tuple of len 4,
               it determines how shiny the highlights produced by this light will be.

           ambient is a list or tuple of len 4,
                it is the color of the normal light that comes from all directions equally
                and is scattered across the scene uniformally.

           diffuse is a list or tuple of len 4,
               it determines the color of a specific direction source - like the sun -
               and it will light objects more intensely the more they face towards it.

           shininess is an int > 0 < 128, that determines how widespread(for a low number),
               or how concentrated(for a high number) the specular light is applied.

           directional must be 0, 1, True or False - used to determine whether the
               light fills everywhere - like a lightbulb,
               or only in one direction - like a flashlight."""

        self.position = position
        self.specular = specular
        self.ambient = ambient
        self.diffuse = diffuse
        self.shininess = shininess

        self.directional = directional

        self.light_num = int(self.num_lights)
        self.num_lights += 1

        self.compile()

    def __get_pos(self):
        """This method returns the position <i>plus</i> directional of the light"""

        return self.position[0], self.position[1], self.position[2], -int(self.directional)

    def compile(self):
        """This method compiles the light to a GL_LIGHT(n),
           using the parameters stored here."""
        exec "kind = GL_LIGHT" + str(self.light_num) #yes, I'm using the evil exec, but it saves about
                                                     #40+ lines of code here.
        glEnable(kind)
        glMaterialfv( GL_FRONT_AND_BACK, GL_SPECULAR, self.specular )
        glMaterialfv( GL_FRONT_AND_BACK, GL_AMBIENT, self.ambient )
        glMaterialfv( GL_FRONT_AND_BACK, GL_SHININESS, self.shininess )
        glLightfv(kind, GL_AMBIENT, self.ambient)
        glLightfv(kind, GL_DIFFUSE, self.diffuse)
        glLightfv(kind, GL_SPECULAR, self.specular)
        glLightfv(kind, GL_POSITION, self.__get_pos())

        return None
