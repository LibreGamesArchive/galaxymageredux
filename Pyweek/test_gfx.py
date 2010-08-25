import pygame
from pygame.locals import *

from lib import gfx_engine, event

def main():
    pygame.init()
    screen = pygame.display.set_mode((640,480))

    event_handler = event.Handler()

    eng = gfx_engine.GFXEngine(screen, 'main')

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

        if my < 5:
            eng.camera.move(0, -0.1)
        elif my > 475:
            eng.camera.move(0, 0.1)

        print eng.mapd.get_mouse_tile()

        screen.fill((0,0,0))
        eng.render()
        pygame.display.flip()

main()
