import pygame
from pygame.locals import *

from lib import event, gui
import random

def main():
    pygame.init()
    screen = pygame.display.set_mode((640,480))

    event_handler = event.Handler()
    main_app = gui.App(screen, event_handler)

    some_cont = gui.Container(main_app, (300,100), (50,50))
    some_cont.bg_color = (255,255,255, 150)

    butt = gui.Button(some_cont, (5,5), "test")
    text_box = gui.MessageBox(main_app, (300,100), (50, 200))
    text_box.bg_color = (255,0,0,150)

    butt.dispatch.bind('click', lambda: text_box.add_line('test'+str(random.randint(0,45))))

    inp = gui.Input(some_cont, 290, (5,25))

    popup = gui.PopUp(butt, text="adds text to the message box below", width=100)
    popup.bg_color = (255,255,255,100)

    drop = gui.DropDown(main_app, (5, 5), "press me!")
    drop.setChild(gui.Label(main_app, (0,0), 'woah!'))

    while 1:
        event_handler.update()

        if event_handler.quit:
            pygame.quit()
            return None

        screen.fill((0,0,0))
        main_app.render()
        pygame.display.flip()

main()
