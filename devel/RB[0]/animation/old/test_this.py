import core
from core import *

##import new_obj_loader as obj_loader
import obj_loader
reload(obj_loader)


def main():
    core.init()
    core.set3d()

    c = Camera()
    c.distance = 100

    l = Light((0,0,-15),
              (1,1,1,1),
              (1,1,1,1),
              (1,1,1,1))

    obj = obj_loader.load_obj("test_mesh.obj")

    clear_screen()
    c.update()

    obj.render((0,0,0))

    glBegin(GL_LINES)
    glColor4f(1, 0, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(10, 0, 0)
    glEnd()
    pygame.display.flip()

main()
