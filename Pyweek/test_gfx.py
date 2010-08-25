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

        screen.fill((0,0,0))
        eng.render()
        pygame.display.flip()

main()
