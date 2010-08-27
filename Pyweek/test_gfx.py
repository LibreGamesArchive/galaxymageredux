import pygame
from pygame.locals import *

from lib import gfx_engine, event, mod_base

def main():
    pygame.init()
    screen = pygame.display.set_mode((640,480))

    event_handler = event.Handler()

    eng = gfx_engine.GFXEngine(screen, 'main')
    if eng.failed:
        return

    units = mod_base.UnitHandler()
    units.load_dir('data/scenarios/main/units/')
    units.load_dir('data/units/')
    print units.units

    m_tile = eng.mapd.make_entity('gui_mouse-hover.png', (0,0))

    while 1:
        event_handler.update()

        if event_handler.quit:
            pygame.quit()
            return None

        mx, my = event_handler.mouse.get_pos()
        if mx < 5:
            eng.camera.move(-0.1, 0)
        elif mx > 635:
            eng.camera.move(0.1, 0)
        else:
            print(eng.mapd.get_mouse_tile())

        if my < 5:
            eng.camera.move(0, -0.1)
        elif my > 475:
            eng.camera.move(0, 0.1)
        else:
            print(eng.mapd.get_mouse_tile())

        x, y = eng.mapd.get_mouse_tile()
        m_tile.pos = (x,y)
        
        screen.fill((0,0,0))
        eng.render()
        pygame.display.flip()

main()
