
import pygame
from pygame.locals import *
from lib import SLG, event, gui

class Engine(SLG.Client):
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
        lil_font = pygame.font.Font(None, 20)

        gamel = gui.Label(self.main_app, (5,5), 'Games:')
        gamel.text_color = (200,200,200)
        gamel.bg_color = (0,0,0,0)
        desc = gui.Label(self.main_app, gui.RelativePos(to=gamel), 'name <scenario> [master] (players / max) CAN JOIN')
        desc.text_color = (200,200,200)
        desc.bg_color = (0,0,0,0)
        desc.font = lil_font

        self.game_list_cont = gui.Container(self.main_app, (440, (lil_font.get_height()+2)*10), gui.RelativePos(to=desc,pady=5))
        self.game_list_cont.font = lil_font
        self.game_list_cont.bg_color = (200,100,100)

        self.game_list_select = gui.Menu(self.game_list_cont, (0,0), padding=(2,2))
        self.game_list_select.entry_bg_color = (200,75,75)
        self.game_list_list = []
        self.game_list_page = 0

        game_list_ppage = gui.Button(self.main_app, gui.RelativePos(to=self.game_list_cont, y='bottom', pady=5), 'Last Page')
        game_list_ppage.dispatch.bind('click', lambda: self.view_game_page(self.game_list_page-1))

        self.game_list_lpage = gui.Label(self.main_app, gui.RelativePos(to=game_list_ppage, x='right', y='top', padx=5), 'Page: 0')

        game_list_npage = gui.Button(self.main_app, gui.RelativePos(to=self.game_list_lpage, x='right', y='top', padx=5), 'Next Page')
        game_list_npage.dispatch.bind('click', lambda: self.view_game_page(self.game_list_page+1))

        self.pre_conn_app.activate()
        SLG.Client.__init__(self, "changeme", SLG.main_server_host, SLG.main_server_port)

    def handle_connect(self, *args, **kwargs):
        text = self.get_username.text

        if len(text)>5:
            self.username = text
            self.connect()
            self.main_app.activate()

    def connected(self, avatar):
        SLG.Client.connected(self, avatar)
        self.avatar.callRemote('getGameList')

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

    def view_game_page(self, num):
        if num < 0:
            num = 0
        if num > len(self.game_list_list.values())*0.1:
            num = int(len(self.game_list_list.values())*0.1)

        self.game_list_page = num
        opts = []
        for game in sorted(self.game_list_list.values())[num*10:(num+1)*10]:
            game_id, name, scenario, master, players, max_players, in_game = game
            l = str(name) + ' <' + str(scenario) + '> ' + '[' + str(master) + '] '
            l += '(' + str(players) + ' / ' + str(max_players) + ')'
            if in_game:
                l+= ' -- CLOSED'
            else:
                l+= ' -- OPEN'
            opts.append(l)

        self.game_list_select.options = opts
        self.game_list_select.build_options()
        self.game_list_lpage.text = 'Page: %s'%num

    def remote_sendGameList(self, games):
        self.game_list_list = {}
        for game in games:
            game_id, name, scenario, master, players, max_players, in_game = game
            l = str(name) + ' <' + str(scenario) + '> ' + '[' + str(master) + '] '
            l += '(' + str(players) + ' / ' + str(max_players) + ')'
            if in_game:
                l+= ' -- CLOSED'
            else:
                l+= ' -- OPEN'
            self.game_list_list[l] = game

        self.view_game_page(self.game_list_page)

def main():
    g = Engine()

main()
