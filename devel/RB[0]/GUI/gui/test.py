
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

    main_win = gui.Window(app, (640, 40), "MainWindow", "topright",
                          [600, 440], caption="Main Window!",
                          icon = "label.png")

    scroll = gui.ScrollBar(app, (640, -1), "Scroller1", "midright", None,
                           (15, 100*2), (15, 100),
                           0, 1)

    label = gui.Label(main_win, (50, 50), "Label1", "Test Label",
                      icon="label.png")
    button = gui.Button(main_win, (100, -1), "Button1", "Quit!",
                        icon="label.png")
    b2 = gui.Button(main_win, (-1, 50), "Button2", "Button2",
                        icon="label.png")

    menu = gui.Menu(main_win, (-1, -1), "Menu1", "A Menu",
                  ["tttt1", "tttttttt2", "3"],
                    icon="label.png", icons={"tttt1":"label.png",
                                             "tttttttt2":"label.png",
                                             "3":"label.png"})
    blist = gui.MenuList(main_win, (600, 440), "ButtonList",
                         ["play", "help", "exit"],
                         widget_pos="bottomright",
                         icons={"play":"label.png",
                                "help":"label.png",
                                "exit":"label.png"})

    inp = gui.TextInputBox(main_win, (0, 440), "Input1",
                           "input", "type your input",
                           widget_pos="bottomleft")

    win = gui.Window(main_win, (-1, -1), "Window1", "topleft",
                     [150, 150],
                     caption="window", icon="label.png")
    subbutton1 = gui.Button(win, (-1, -1), "SubB1", "Button!",
                            widget_pos="center")
    suni = gui.TextInputBox(win, (0, 150), "In2", "prompt",
                            "hello :)", widget_pos="bottomleft")

    pygame.key.set_repeat(50)

    while 1:
        for event in app.get_events():
            if event.type == gui.GUI_EVENT:
                if event.widget == gui.Window:
                    if event.name == "MainWindow":
                        event = event.subevent
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
                        if event.widget == gui.Window:
                            if event.name == "Window1":
                                event = event.subevent
                                if event.widget == gui.Button:
                                    print "Window1:", event.name
                                if event.widget == gui.TextInputBox:
                                    print "Window1: Input:", event.string
        print scroll.get_value()
        screen.blit(app.render(), (0, 0))
        pygame.display.flip()


main()
