import pygame
from pygame.locals import *

import event
import gui

def main():
    pygame.init()
    screen = pygame.display.set_mode((640,480))

    event_handler = event.Handler()
    main_app = gui.App(screen, event_handler)

    some_cont = gui.Container(main_app, (300,100), (50,50))
    some_cont.bg_color = (255,255,255, 150)

    butt = gui.Button(some_cont, (5,5), "test")

    while 1:
        event_handler.update()

        if event_handler.quit:
            pygame.quit()
            return None

        screen.fill((0,0,0))
        main_app.render()
        pygame.display.flip()

main()
