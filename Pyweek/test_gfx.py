import pygame
from pygame.locals import *

from lib import gfx_engine

def main():
    pygame.init()
    screen = pygame.display.set_mode((640,480))

    eng = gfx_engine.GFXEngine(screen, 'main')
    eng.render()
    pygame.display.flip()

main()
