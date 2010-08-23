import pygame
from pygame.locals import *

from lib import event, gui, net
import random

class Engine(net.Client):
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((640,480))

        self.event_handler = event.Handler()
        self.main_app = gui.App(self.screen, self.event_handler)

        self.message_box = gui.MessageBox(self.main_app, (630,100), (5,5))
        self.message_box.bg_color = (255,100,100)

        self.input_box = gui.Input(self.main_app, 300, (5,110))
        self.input_box.bg_color = (255,0,0)
        self.input_box.text_color = (0,0,0)
        self.input_button = gui.Button(self.main_app, (310, 110), 'Submit')
        self.input_button.bg_color = (255,0,0)
        self.input_button.text_hover_color = (100,100,100)
        self.input_button.text_click_color = (200,200,200)

        self.input_box.dispatch.bind("input-submit", self.handle_input)
        self.input_button.dispatch.bind("click", self.handle_input)

        self.conn_button = gui.Button(self.main_app, (self.input_button.size[0]+315, 110), "Connect")
        self.conn_button.dispatch.bind("click", lambda:(self.connect(), self.conn_button.destroy()))

        net.Client.__init__(self, "localhost", 44444, "test!")

    def handle_input(self, *args, **kwargs):
        text = self.input_box.text
        self.input_box.text = ""
        self.input_box.cursor_pos = 0

        if text and self.avatar:
            self.avatar.callRemote('sendMessage', text)

    def update(self):
        self.event_handler.update()
        if self.event_handler.quit:
            pygame.quit()
            self.disconnect()
            self.close()
            return None

        self.screen.fill((0,0,0))
        self.main_app.render()
        pygame.display.flip()

    def remote_getMessage(self, user_type, name, message):
        self.message_box.add_line(name+': '+message)

def main():
    g = Engine()

main()
