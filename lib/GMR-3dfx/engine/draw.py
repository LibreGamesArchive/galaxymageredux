import include
from include import *

import display
import misc


def rect2d(area, color=(1,1,1,1), texture=None, tex_scale=True):
    area = pygame.Rect(area)

    if texture==None:
        texture = display.get_display().blank_texture

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

    glColor4f(*misc.Color(color).get_rgba1())
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

def lines2d(pairs, color=(1,1,1,1)):
    glColor4f(*misc.Color(color).get_rgba1())
    glBegin(GL_LINES)
    for pair in pairs:
        glVertex3f(pair[0][0], pair[0][1], 0)
        glVertex3f(pair[1][0], pair[1][1], 0)
    glEnd()
