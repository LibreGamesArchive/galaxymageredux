
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
    label = gui.Label(app, (50, 50), "Label1", "Test Label",
                      icon="label.png")
    button = gui.Button(app, (100, -1), "Button1", "Quit!",
                        icon="label.png")
    b2 = gui.Button(app, (-1, 50), "Button2", "Button2",
                        icon="label.png")

    menu = gui.Menu(app, (-1, -1), "Menu1", "A Menu",
                  ["tttt1", "tttttttt2", "3"],
                    icon="label.png", icons={"tttt1":"label.png",
                                             "tttttttt2":"label.png",
                                             "3":"label.png"})
    blist = gui.MenuList(app, (640, 480), "ButtonList",
                         ["play", "help", "exit"],
                         widget_pos="bottomright",
                         icons={"play":"label.png",
                                "help":"label.png",
                                "exit":"label.png"})

    inp = gui.TextInputBox(app, (0, 480), "Input1",
                           "input", "type your input",
                           widget_pos="bottomleft")

    win = gui.WindowBar(app, (640, -1), "WinB1", "midright",
                        caption="A movable window bar!")
    win_button = gui.Button(app, (640, 290), "WinButton1", "AttachedToAWindow!",
                            widget_pos="midright")
    win.attach(win_button)

    pygame.key.set_repeat(50)

    while 1:
        for event in app.get_events():
            if event.type == gui.GUI_EVENT:
                if event.widget == gui.Button:
                    if event.name == "Button1":
                        if event.action == gui.GUI_EVENT_CLICK:
                            pygame.quit()
                            return
                    if event.name == "Button2":
                        if event.action == gui.GUI_EVENT_CLICK:
                            print "Hello :)"
                if event.widget == gui.Menu:
                    if event.name == "Menu1":
                        if event.action == gui.GUI_EVENT_CLICK:
                            print event.entry
                if event.widget == gui.MenuList:
                    if event.name == "ButtonList":
                        if event.action == gui.GUI_EVENT_CLICK:
                            print event.entry
                if event.widget == gui.TextInputBox:
                    if event.name == "Input1":
                        if event.action == gui.GUI_EVENT_INPUT:
                            print event.string
        screen.blit(app.render(), (0, 0))
        pygame.display.flip()


main()
