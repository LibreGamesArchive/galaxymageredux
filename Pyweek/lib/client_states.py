import pygame
from pygame.locals import *
import SLG, event, gui, load_mod_file, in_game
import glob, os


class Main(SLG.Client):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640,480))

        self.scenario_list = self.get_scenarios()
        self.clock = pygame.time.Clock()

        self.cur_state = Connect(self)

        SLG.Client.__init__(self, "changeme",
                            SLG.main_server_host,
                            SLG.main_server_port)

    def close_app(self):
        pygame.quit()
        self.disconnect()
        self.close()

    def get_scenarios(self):
        l = glob.glob('data/scenarios/*')
        n = []
        for i in l:
            n.append(os.path.split(i)[1])
        return n

    def remote_OverrideUsername(self, name):
        self.username = name

    def connected(self, avatar):
        SLG.Client.connected(self, avatar)
        self.cur_state = ServerLobby(self)

    def remote_joinedGame(self, name, scenario, team):
        self.cur_state = GameRoomLobby(self, name, scenario, team)

    def disconnected(self):
        #self.pre_conn_app.activate()
        #TODO: make some kind of message screen first!

        self.close_app()
        raw_input('Connection to server lost!')

    def update(self):
        self.clock.tick(30)
        pygame.display.set_caption(str(self.clock.get_fps()))

        self.cur_state.update()

    def remote_getMessage(self, player, message):
        self.cur_state.remote_getMessage(player, message)

    def sendMessage(self, message):
        self.avatar.callRemote('sendMessage', message)

    def remote_sendGameList(self, games):
        self.cur_state.remote_sendGameList(games)

    def remote_sendLobbyUsersList(self, users):
        self.cur_state.remote_sendLobbyUsersList(users)

    def remote_cannotJoinGame(self, reason):
        self.cur_state.remote_cannotJoinGame(reason)

    def remote_getTalkFromServer(self, command, args):
        self.cur_state.remote_getTalkFromServer(command, args)

class State(object):
    def __init__(self, engine):
        self.engine = engine
        self.screen = self.engine.screen
        self.scenario_list = self.engine.scenario_list
        self.event_handler = event.Handler()

        self.app = gui.App(self.screen, self.event_handler)

    def update(self):
        self.event_handler.update()

        if self.event_handler.quit:
            self.engine.close_app()
            return None

        self.screen.fill((0,0,0))
        self.app.render()
        pygame.display.flip()

    def remote_getMessage(self, player, message):
        pass

    def sendMessage(self, message):
        self.engine.sendMessage(message)

    def remote_sendGameList(self, games):
        pass

    def remote_sendLobbyUsersList(self, users):
        pass

    def remote_cannotJoinGame(self, reason):
        pass

    def remote_joinedGame(self, name, scenario, team):
        pass

    def remote_getTalkFromServer(self, command, args):
        pass

class Connect(State):
    def __init__(self, engine):
        State.__init__(self, engine)

        lil_font = pygame.font.Font(None, 20)
        small_font = pygame.font.Font(None, 25)

        #pre connection login/etc.
        x=gui.Label(self.app, (5,75), 'Connect to a server!')
        x.bg_color = (0,0,0,0)
        x.text_color = (255,255,255)

        cont = gui.Container(self.app, (300, 200), gui.RelativePos(to=x, pady=5))
        cont.bg_color = (100,100,255,100)
        cont.font = small_font

        x=gui.Label(cont, (5,5), 'Username:')
        x.bg_color = (0,0,0,0)
        x.text_color = (100,100,100)

        self.get_username = gui.Input(cont,
                                      210, gui.RelativePos(to=x, pady=5, padx=5),
                                      max_chars=20)
        self.get_username.always_active=False
        self.get_username.bg_color = (200,200,200)
        self.get_username.text_color = (100,100,100)

        x=gui.Label(cont, gui.RelativePos(to=self.get_username, pady=5, padx=-5), "Server:")
        x.bg_color = (0,0,0,0)
        x.text_color = (100,100,100)

        self.connect_server_drop = gui.DropDownMenu(cont, gui.RelativePos(to=x, pady=5, padx=5),
                                                    'main', ['main', 'local', 'other'])
        self.connect_server_drop.bg_color=(100,100,100)
        self.connect_server_serv = gui.Input(cont,
                                             200,
                                             gui.RelativePos(to=self.connect_server_drop, x='right', y='top',padx=5),
                                             -1)
        self.connect_server_serv.bg_color = (200,200,200)
        self.connect_server_serv.text_color = (100,100,100)
        self.connect_server_serv.always_active = False
        self.connect_server_serv.visible = False
        self.connect_server_serv.text = str(SLG.main_server_host)
        self.connect_server_drop.dispatch.bind('select', self.handle_server_sel)

        x=gui.Label(cont, gui.RelativePos(to=self.connect_server_drop, pady=5, padx=-5), "Port:")
        x.bg_color = (0,0,0,0)
        x.text_color = (100,100,100)

        self.connect_port_drop = gui.DropDownMenu(cont, gui.RelativePos(to=x, pady=5, padx=5),
                                                  'default', ['default', 'other'])
        self.connect_port_drop.bg_color = (100,100,100)
        self.connect_port_serv = gui.Input(cont,
                                             200,
                                             gui.RelativePos(to=self.connect_port_drop, x='right', y='top',padx=5),
                                             -1)
        self.connect_port_serv.bg_color = (200,200,200)
        self.connect_port_serv.text_color = (100,100,100)
        self.connect_port_serv.always_active = False
        self.connect_port_serv.visible = False
        self.connect_port_serv.text=str(SLG.main_server_port)
        self.connect_port_drop.dispatch.bind('select', self.handle_port_sel)

        self.connect_button = gui.Button(cont, gui.RelativePos(to=self.connect_port_drop, pady=5, padx=-5), 'Connect')
        self.connect_button.font = self.app.font
        self.connect_button.bg_color = (255,0,0)
        self.connect_button.text_hover_color = (100,100,100)
        self.connect_button.text_click_color = (200,200,200)

        self.get_username.dispatch.bind("input-submit", self.handle_connect)
        self.connect_button.dispatch.bind("click", self.handle_connect)
        popup = gui.PopUp(self.connect_button, text='Username must be between 4 and 20 characters long!')
        popup.bg_color = (255,255,255,100)
        #end pre conn

    def handle_connect(self, *args, **kwargs):
        text = self.get_username.text

        if len(text)>=4:
            self.engine.username = text
            self.engine.hostname = self.connect_server_serv.text
            self.engine.port = int(self.connect_port_serv.text)
            self.engine.connect()

    def set_default_input(self, widg, inp):
        widg.text = inp
        widg.cursor_pos = len(inp)
    def handle_server_sel(self, value):
        if value == 'main':
            self.connect_server_serv.text = SLG.main_server_host
            self.connect_server_serv.visible = False
        elif value == 'local':
            self.connect_server_serv.text = 'localhost'
            self.connect_server_serv.visible = False
        elif value == 'other':
            self.connect_server_serv.text = SLG.main_server_host
            self.connect_server_serv.visible = True
            self.connect_server_serv.cursor_pos = len(SLG.main_server_host)
        self.connect_server_drop.text = value
    def handle_port_sel(self, value):
        if value == 'default':
            self.connect_port_serv.text = str(SLG.main_server_port)
            self.connect_port_serv.visible = False
        elif value == 'other':
            self.connect_port_serv.text = str(SLG.main_server_port)
            self.connect_port_serv.visible = True
            self.connect_port_serv.cursor_pos = len(SLG.main_server_host)
        self.connect_port_drop.text = value


class ServerLobby(State):
    def __init__(self, engine):
        State.__init__(self, engine)

        lil_font = pygame.font.Font(None, 20)
        small_font = pygame.font.Font(None, 25)

        #server lobby view
        gamel = gui.Label(self.app, (5,75), 'Games:')
        gamel.text_color = (200,200,200)
        gamel.bg_color = (0,0,0,0)
        desc = gui.Label(self.app, gui.RelativePos(to=gamel), 'name <scenario> [master] (players / max) CAN JOIN')
        desc.text_color = (200,200,200)
        desc.bg_color = (0,0,0,0)
        desc.font = lil_font

        self.game_list_cont = gui.Container(self.app, (440, (lil_font.get_height()+2)*10), gui.RelativePos(to=desc,pady=5))
        self.game_list_cont.font = lil_font
        self.game_list_cont.bg_color = (200,100,100)

        self.game_list_select = gui.DisableMenu(self.game_list_cont, (0,0), padding=(2,2))
        self.game_list_select.entry_bg_color = (200,75,75)
        self.game_list_select.dispatch.bind('select', self.handle_game_list_select)

        self.game_list_list = {}
        self.game_list_page = 0
        self.game_list_id = {}

        game_list_ppage = gui.Button(self.app, gui.RelativePos(to=self.game_list_cont, pady=10, padx=5), 'Last')
        game_list_ppage.dispatch.bind('click', lambda: self.view_game_page(self.game_list_page-1))

        self.game_list_lpage = gui.Label(self.app, gui.RelativePos(to=game_list_ppage, x='right', y='top', padx=5), 'Page: 0')
        self.game_list_lpage.bg_color = (0,0,0,0)
        self.game_list_lpage.text_color = (100,100,100)

        game_list_npage = gui.Button(self.app, gui.RelativePos(to=self.game_list_lpage, x='right', y='top', padx=5), 'Next')
        game_list_npage.dispatch.bind('click', lambda: self.view_game_page(self.game_list_page+1))

        game_list_ngame = gui.Button(self.app, gui.RelativePos(to=game_list_npage, x='right', y='top', padx=5), 'Create Game')
        game_list_ngame.dispatch.bind('click', self.handle_lobby_create_game_room)

        self.popup_bads_cont = gui.Container(self.app, (5,5), (0,0))
        self.popup_bads_cont.visible = False
        self.popup_bads_cont.bg_color = (255,255,255,175)
        self.popup_bads = {'ingame': "You cannot join this game room because it is already in progress",
                           'full': "You cannot join this game room because it is full",
                           'scen': "You cannot join this game room because you don't have the required scenario"}
        self.popup_bads_label = gui.Label(self.popup_bads_cont, (5,15), self.popup_bads['scen'])
        self.popup_bads_label.bg_color=(0,0,0,0)
        self.popup_bads_label.font = lil_font
        w,h = self.popup_bads_label.get_size()
        self.popup_bads_cont.change_size((w+10, h+30))
        self.popup_bads_cont.dispatch.bind('unfocus', lambda:self.turn_off_widget(self.popup_bads_cont))

        self.server_lobby_messages = gui.MessageBox(self.app, (440, 100),
                                                    gui.RelativePos(to=game_list_ppage, pady=30, padx=-5))
        self.server_lobby_messages.bg_color = (200,75,75)
        self.server_lobby_messages.font = lil_font
        self.server_lobby_input = gui.Input(self.app, 350, gui.RelativePos(to=self.server_lobby_messages, pady=5),
                                            max_chars=30)
        self.server_lobby_input.bg_color = (200,75,75)
        self.server_lobby_input.text_color = (0,0,0)
        self.server_lobby_input.font = lil_font
        self.server_lobby_binput = gui.Button(self.app,
                                              gui.RelativePos(to=self.server_lobby_input, padx=5,x='right',y='top'),
                                              'Submit')
        self.server_lobby_binput.bg_color=(200,200,200)
        self.server_lobby_input.dispatch.bind('input-submit', self.lobby_submit_message)
        self.server_lobby_binput.dispatch.bind('click', self.lobby_submit_message)

        cont = gui.Container(self.app, (185, 470), (450, 5))
        cont.bg_color = (100,100,255,100)
        l = gui.Label(cont, (5, 5), 'Users in Lobby:')
        l.bg_color=(0,0,0,0)
        l.text_color=(100,100,100)

        self.server_lobby_users = gui.List(cont, gui.RelativePos(to=l, pady=5))
        self.server_lobby_users.font = lil_font
        self.server_lobby_users.entry_bg_color = (0,0,0,0)
        #end server lobby view

        self.engine.avatar.callRemote('getGameList')

    def lobby_submit_message(self, *args):
        message = self.server_lobby_input.text
        if message:
            self.sendMessage(message)
            self.server_lobby_input.text = ''
            self.server_lobby_input.cursor_pos = 0
    def turn_off_widget(self, widg):
        widg.visible = False
    def turn_on_widget(self, widg):
        widg.visible = True

    def handle_game_list_select(self, value, disabled):
        game = self.game_list_list[value]
        game_id, name, scenario, master, players, max_players, in_game = game

        if not scenario in self.scenario_list:
            self.turn_on_widget(self.popup_bads_cont)
            self.popup_bads_label.text = self.popup_bads['scen']
            self.popup_bads_cont.pos.x = 10
            self.popup_bads_cont.pos.y = pygame.mouse.get_pos()[1]
            self.popup_bads_cont.focus()
        else:
            self.engine.avatar.callRemote('requestJoinGame', game_id, self.scenario_list)

    def handle_lobby_create_game_room(self):
        self.engine.cur_state = MakeGameRoom(self.engine)

    def view_game_page(self, num):
        if num < 0:
            num = 0
        if num > len(self.game_list_list.values())*0.1:
            num = int(len(self.game_list_list.values())*0.1)

        self.game_list_page = num
        opts = []
        for game in sorted(self.game_list_list.keys())[num*10:(num+1)*10]:
            game_id, name, scenario, master, players, max_players, in_game = self.game_list_list[game]
            l = ''
            if in_game:
                l += '    '
            l += str(name) + ' <' + str(scenario) + '> ' + '[' + str(master) + '] '
            l += '(' + str(players) + ' / ' + str(max_players) + ')'
            if in_game or players==max_players:
                l+= ' -- CLOSED'
                dis = True
            else:
                l+= ' -- OPEN'
                dis = False
            opts.append((l, dis))

        self.game_list_select.options = opts
        self.game_list_select.build_options()
        self.game_list_lpage.text = 'Page: %s'%num

    def remote_sendGameList(self, games):
        self.game_list_list = {}
        for game in games:
            game_id, name, scenario, master, players, max_players, in_game = game
            l = ''
            if in_game:
                l += '    '
            l += str(name) + ' <' + str(scenario) + '> ' + '[' + str(master) + '] '
            l += '(' + str(players) + ' / ' + str(max_players) + ')'
            if in_game or players==max_players:
                l+= ' -- CLOSED'
            else:
                l+= ' -- OPEN'
            self.game_list_list[l] = game

        self.view_game_page(self.game_list_page)

    def remote_sendLobbyUsersList(self, users):
        self.server_lobby_users.entries = users
        self.server_lobby_users.build_entries()
    def remote_cannotJoinGame(self, reason):
        self.turn_on_widget(self.popup_bads_cont)
        self.popup_bads_label.text = self.popup_bads[reason]
        self.popup_bads_cont.pos.x = 10
        self.popup_bads_cont.pos.y = pygame.mouse.get_pos()[1]
        self.popup_bads_cont.focus()

    def remote_getMessage(self, player, message):
        self.server_lobby_messages.add_line('%s: %s'%(player, message))

class MakeGameRoom(State):
    def __init__(self, engine):
        State.__init__(self, engine)

        lil_font = pygame.font.Font(None, 20)
        small_font = pygame.font.Font(None, 25)

        #make game room view
        x=gui.Label(self.app, (5,75), 'Make a Game')
        x.bg_color = (0,0,0,0)
        x.text_color = (255,255,255)

        cont = gui.Container(self.app, (300, 200), gui.RelativePos(to=x, pady=5))
        cont.bg_color = (100,100,255,100)
        cont.font = small_font

        x=gui.Label(cont, (5,5), 'Game name:')
        x.bg_color = (0,0,0,0)
        x.text_color = (255,255,255)

        self.game_room_make_name = gui.Input(cont, 210, gui.RelativePos(to=x, padx=5, pady=5), max_chars=20)
        self.game_room_make_name.always_active=False
        self.game_room_make_name.bg_color = (200,200,200)
        self.game_room_make_name.text_color = (100,100,100)
        self.game_room_make_name.dispatch.bind('input-submit', self.handle_game_make_room)

        x=gui.Label(cont, gui.RelativePos(to=self.game_room_make_name, padx=-5, pady=5), 'Pick Scenario:')
        x.bg_color = (0,0,0,0)
        x.text_color = (255,255,255)

        self.game_room_make_scen = gui.DropDownMenu(cont, gui.RelativePos(to=x, pady=5, padx=5), self.scenario_list[0],
                                                    self.scenario_list)
        self.game_room_make_scen.bg_color = (100,100,100)
        self.game_room_make_scen.dispatch.bind('select', self.handle_game_scen_sel)

        self.game_room_make_butt = gui.Button(cont, (5,160),
                                              "Make Game")
        self.game_room_make_butt.dispatch.bind('click', self.handle_game_make_room)
        #end make game room view

    def handle_game_scen_sel(self, value):
        self.game_room_make_scen.text = value
    def handle_game_make_room(self, *args):
        name = self.game_room_make_name.text
        if len(name) < 4:
            return None
        scen = self.game_room_make_scen.text
        self.engine.avatar.callRemote('makeGame', name, scen, self.scenario_list)

class GameRoomLobby(State):
    def __init__(self, engine, name, scenario, team):
        State.__init__(self, engine)

        self.cur_game = GameEngine(self)
        self.cur_game.scenario = scenario
        self.cur_game.my_team = team
        self.cur_game.am_master = False
        self.cur_game.game_name = name

        lil_font = pygame.font.Font(None, 20)
        small_font = pygame.font.Font(None, 25)

        #game room lobby view
        self.game_room_lobby_game_name = gui.Label(self.app,
            (5,5), 'game name: <game name>')
        self.game_room_lobby_game_name.bg_color = (0,0,0,0)
        self.game_room_lobby_game_name.text_color = (100,100,100)

        self.game_room_lobby_scenario = gui.Label(self.app,
            gui.RelativePos(to=self.game_room_lobby_game_name,pady=5),
            'scenario: <scenario>')
        self.game_room_lobby_scenario.bg_color = (0,0,0,0)
        self.game_room_lobby_scenario.text_color = (100,100,100)

        self.game_room_lobby_sel_scenario = gui.DropDownMenu(self.app,
            gui.RelativePos(to=self.game_room_lobby_scenario,
                            x='right', y='top', padx=5),
            'change scenario', self.scenario_list)
        self.game_room_lobby_sel_scenario.visible = False

        self.game_room_lobby_num_players = gui.Label(self.app,
            gui.RelativePos(to=self.game_room_lobby_scenario,pady=5),
            'players (0/0)')
        self.game_room_lobby_num_players.bg_color = (0,0,0,0)
        self.game_room_lobby_num_players.text_color = (100,100,100)

        self.game_room_lobby_players = gui.GameRoomLobbyPlayers(
            self.app, (400, 250),
            gui.RelativePos(to=self.game_room_lobby_num_players, pady=5))
        self.game_room_lobby_players.bg_color = (210,100,100)
        self.game_room_lobby_players.dispatch.bind('kick', self.game_room_lobby_kick)
        self.game_room_lobby_players.dispatch.bind('change-team', self.game_room_lobby_change_team)
        self.game_room_lobby_players.font = lil_font

        self.game_room_lobby_messages = gui.MessageBox(
            self.app, (400, 100), gui.RelativePos(to=self.game_room_lobby_players, pady=5))
        self.game_room_lobby_messages.bg_color = (200,75,75)
        self.game_room_lobby_messages.font = lil_font

        self.game_room_lobby_input = gui.Input(
            self.app, 350, gui.RelativePos(to=self.game_room_lobby_messages, pady=5))
        self.game_room_lobby_input.bg_color = (200,75,75)
        self.game_room_lobby_input.text_color = (0,0,0)
        self.game_room_lobby_input.font = lil_font

        self.game_room_lobby_binput = gui.Button(
            self.app, gui.RelativePos(to=self.game_room_lobby_input, x='right',y='top',padx=5),
            'Submit')
        self.game_room_lobby_binput.bg_color=(200,200,200)
        self.game_room_lobby_input.dispatch.bind('input-submit', self.game_room_submit_message)
        self.game_room_lobby_binput.dispatch.bind('click', self.game_room_submit_message)

        self.game_room_lobby_start = gui.Button(
            self.app, (500, 400), 'Start Game')
        self.game_room_lobby_start.visible = False
        self.game_room_lobby_start.dispatch.bind('click', lambda self=self: self.cur_game.masterStartGame())

    def remote_getTalkFromServer(self, command, args):
        self.cur_game.getTalkFromServer(command, args)
    def game_room_lobby_kick(self, name):
        self.cur_game.masterKickPlayer(name)
    def game_room_lobby_change_team(self, name):
        self.cur_game.changeTeam(name)
    def game_room_submit_message(self, *args):
        text = self.game_room_lobby_input.text
        if text:
            self.cur_game.sendMessage(text)
            self.game_room_lobby_input.text = ''
            self.game_room_lobby_input.cursor_pos = 0

    def update(self):
        if self.cur_game.in_game:
            self.cur_game.update_game()
        else:
            State.update(self)


class GameEngine(object):
    def __init__(self, client):
        self.client = client

        self.scenario = 'main'
        self.am_master = False
        self.game_name = ""
        self.my_team = ""
        self.player_name = self.client.engine.username
        self.free_teams = []
        self.players = []
        self.max_players = 2
        self.whos_turn = ""

        self.in_game = False
        self.game_obj = None

        #TODO: when self.client.playing, we need to be running our own
        #update function, with our own App
        #bound to self.client.event_handler

    def update_game(self):
        self.game_obj.update()

    def talkToServer(self, command, args):
        self.client.engine.avatar.callRemote('talkToGame', command, args)

    def youAreNowMaster(self, args):
        self.am_master = True
        self.game_master_submit_scenario_data()
        self.update_player_gui()
        if self.in_game:
            self.game_obj.messages.add_line('<server>: You [%s] are now master'%self.client.engine.username)

    def kickedDueToTooManyPlayers(self, args):
        #TODO: handle kicked
        pass

    def kickedDueToScenario(self, args):
        #TODO: handle kicked
        pass

    def kickedByMaster(self, args):
        #TODO: handle kicked
        pass

    def update_player_gui(self):
        self.client.game_room_lobby_num_players.text = 'players (%s/%s)'%(len(self.players), self.max_players)
        self.client.game_room_lobby_scenario.text = 'scenario: '+self.scenario
        self.client.game_room_lobby_game_name.text = 'game name: '+self.game_name
        self.client.game_room_lobby_players.set_players(
            self, self.players, self.free_teams)
        if self.am_master:
            self.client.game_room_lobby_sel_scenario.visible = True
            self.client.game_room_lobby_start.visible = True
        else:
            self.client.game_room_lobby_sel_scenario.visible = False
            self.client.game_room_lobby_start.visible = False

    def playerNamesTeams(self, args):
        self.players = args
        self.update_player_gui()

    def scenarioChanged(self, args):
        scen, team, max_players = args
        self.scenario = scen
        self.my_team = team
        self.max_players = max_players
        self.update_player_gui()

    def game_master_submit_scenario_data(self):
        path = 'data/scenarios/%s/config.py'%self.scenario
        store = load_mod_file.load(path)
        if store == False:
            print 'failed to load config O.o'
        else:
            self.talkToServer('getGameScenarioInfo', {'name':store.name, 'maxp':store.num_players, 'teams':store.teams})

    def stillFreeTeamNames(self, args):
        self.free_teams = args
        self.update_player_gui()

    def masterKickPlayer(self, name):
        self.talkToServer('kickPlayer', name)

    def getTalkFromServer(self, command, args):
        getattr(self, command)(args)

    def sendMessage(self, message):
        self.talkToServer('player_message', message)

    def getMessage(self, args):
        player, message = args
        if self.in_game:
            self.game_obj.messages.add_line(player+': '+message)
        else:
            self.client.game_room_lobby_messages.add_line(player+': '+message)

    def changeTeam(self, name):
        self.talkToServer('playerTeamChange', name)

    def startGame(self, args):
        self.game_obj = in_game.Game(self)
        self.in_game = True

    def masterStartGame(self):
        self.talkToServer('masterStartGame', None)

    def setPlayerTurn(self, team):
        self.whos_turn = team
