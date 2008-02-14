
import pygame
from pygame.locals import *

import gui
reload(gui)

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    app = gui.App(pygame.Surface((640, 480)))
    mytheme = gui.make_theme("default_theme")
    app.theme = mytheme

    win = gui.Window(app, (640, 480), "Win1", "bottomright", (400, 400), "Main Window")

    area = gui.Area(win, "Area1", size=(400, 400))
    button = gui.Button(app, (50, -1), "Button1", "Quit!",
                        icon="label.png")
##    b2 = gui.Button(area, (-1,-1), "B2", "Hello World, this is meant to crash or something")
    b3 = gui.Button(area, (-1, 500), "B3", "another test ;)")
##    area.check_borders()

    pygame.key.set_repeat(50)

    while 1:
        for event in app.get_events():
            if event.type == gui.GUI_EVENT:
                if event.widget == gui.Button:
                    if event.name == "Button1":
                        if event.action == gui.GUI_EVENT_CLICK:
                            pygame.quit()
                            return

        screen.blit(app.render(), (0, 0))
        pygame.display.flip()


main()
