
import pygame
from pygame.locals import *
from lib import SLS, event, gui

class Engine(SLS.Client):
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((640,480))

        self.event_handler = event.Handler()

        self.pre_conn_app = gui.App(self.screen, self.event_handler)
        gui.Label(self.pre_conn_app, (5,5), 'Username:')
        self.get_username = gui.Input(self.pre_conn_app,
                                      300, (5,55),
                                      max_chars=20)
        self.connect_button = gui.Button(self.pre_conn_app, (310, 55), 'Connect')
        self.connect_button.bg_color = (255,0,0)
        self.connect_button.text_hover_color = (100,100,100)
        self.connect_button.text_click_color = (200,200,200)

        self.get_username.dispatch.bind("input-submit", self.handle_connect)
        self.connect_button.dispatch.bind("click", self.handle_connect)
        popup = gui.PopUp(self.connect_button, text='Username must be between 5 and 20 characters long!')
        popup.bg_color = (255,255,255,100)


        self.main_app = gui.App(self.screen, self.event_handler)
        self.server_list = gui.MessageBox(self.main_app, (400, 470), (5,5))
        self.server_list.bg_color = (255,100,100)



        self.pre_conn_app.activate()
        SLS.Client.__init__(self, "changeme", SLS.main_server_host, SLS.main_server_port)

    def handle_connect(self, *args, **kwargs):
        text = self.get_username.text

        if len(text)>5:
            self.username = text
            self.connect()
            self.main_app.activate()

    def connected(self, avatar):
        SLS.Client.connected(self, avatar)
        self.avatar.callRemote('getGameServerList')

    def update(self):
        self.event_handler.update()
        if self.event_handler.quit:
            pygame.quit()
            self.disconnect()
            self.close()
            return None

        self.screen.fill((0,0,0))
        self.event_handler.gui.render()
        pygame.display.flip()

    def disconnected(self):
        self.close()

    def remote_sendGameServerList(self, _list):
        for i in _list:
            self.server_list.add_line(i[0]+'@'+i[1]+':'+i[2])

def main():
    g = Engine()

main()
