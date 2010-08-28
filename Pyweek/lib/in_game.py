import gfx_engine, gui, mod_base, event
import pygame
from pygame.locals import *

class Game(object):
    def __init__(self, engine):
        self.engine = engine
        self.screen = engine.client.screen

        self.gfx = gfx_engine.GFXEngine(engine.client.screen, engine.scenario)
        self.mod = mod_base.Scenario(self, engine.scenario)

        self.event_handler = event.Handler()

        self.app = gui.App(self.screen,
                           self.event_handler)
        lil_font = pygame.font.Font(None, 20)

        self.messages = gui.MessageBox(self.app,
                                       (630, 75),
                                       (5,5))
        self.messages.max_lines = 5
        self.messages.bg_color = (0,0,0,0)
        self.messages.entry_bg_color = (100,100,255,100)
        self.messages.font = lil_font
        self.messages.no_events = True

        self.input_cont = gui.Container(self.app, (320, 30), (160, 330))
        self.input_cont.bg_color = (100,100,255,200)
        self.input_type = gui.Input(self.input_cont, 225, (5,5))
        self.input_type.bg_color = (0,0,0,0)
        self.input_butt = gui.Button(self.input_cont,
                                     gui.RelativePos(to=self.input_type, x='right', y='top', padx=5),
                                     'Submit')
        self.input_butt.bg_color = (150,150,255,100)

        self.input_cont.visible = False
        self.input_type.dispatch.bind('input-submit', self.handle_input_submit)
        self.input_butt.dispatch.bind('click', self.handle_input_submit)

        self.unit_info = gui.Container(self.app, (150, 150), (5, 325))
        self.unit_info.bg_color = (100,100,255,100)
        self.unit_info.font = lil_font

        self.unit_info_sub = gui.Container(self.unit_info, (150,150), (0,0))
        self.unit_info_sub.bg_color = (0,0,0,0)
        self.ui_icon = gui.Icon(self.unit_info_sub, (5,5), self.gfx.images.images.values()[0])
        self.ui_name = gui.Label(self.unit_info_sub, gui.RelativePos(to=self.ui_icon,x='right',y='top',padx=5,pady=25), 'Name')
        self.ui_hp = gui.Label(self.unit_info_sub, gui.RelativePos(to=self.ui_name, pady=5), 'HP: 10/10')
        self.ui_ap = gui.Label(self.unit_info_sub, gui.RelativePos(to=self.ui_hp, pady=5), 'AP: 10/10')
        self.ui_strength = gui.Label(self.unit_info_sub, gui.RelativePos(to=self.ui_ap, pady=5), 'STR: 10')
        self.unit_info_sub.visible = False

        self.commands = gui.Container(self.app, (150, 150), (485, 325))
        self.commands.bg_color = (100,100,255,100)
        self.commands.font = lil_font

        self.next_unit = gui.Button(self.commands, (5,5), 'Next Unit')
        self.next_unit.dispatch.bind('click', self.goToNextUnit)
        self.end_turn = gui.Button(self.commands, gui.RelativePos(to=self.next_unit, pady=25), 'End Turn')
        self.end_turn.dispatch.bind('click', self.endMyTurn)
        self.leave_game = gui.Button(self.commands, gui.RelativePos(to=self.end_turn, pady=25), 'Leave Game')
        self.leave_game.dispatch.bind('click', self.queryLeaveGame)
        self.commands_active = False

        self.unit_desc = gui.Container(self.app, (320, 100), (160, 375))
        self.unit_desc.bg_color = (100,100,255,100)
        self.unit_desc.font = lil_font
        self.unit_desc_sub = gui.Container(self.unit_desc, (320,100), (0,0))
        self.unit_desc_sub.bg_color = (0,0,0,0)
        self.unit_desc1 = gui.Label(self.unit_desc_sub, (5,5), 'Unit Description:')
        self.unit_desc2 = gui.Label(self.unit_desc_sub, gui.RelativePos(to=self.unit_desc1, pady=5, padx=25), 'Change')
        self.unit_abil1 = gui.Label(self.unit_desc_sub, gui.RelativePos(to=self.unit_desc2, pady=15, padx=-25), 'Unit Abilities')
        self.unit_abil2 = gui.Label(self.unit_desc_sub, gui.RelativePos(to=self.unit_abil1, pady=5, padx=25), 'Change')
        self.unit_desc_sub.visible = False

        self.leave_game = gui.Container(self.app, (640,480), (0,0))
        self.leave_game.bg_color = (255,255,255,100)

        self.leave_game_question = gui.Label(self.leave_game, (100, 200), 'Do you really want to leave the game?!?!')
        self.leave_game_question.text_color = (255,255,255)
        self.do_leave_game = gui.Button(self.leave_game, (200, 240), 'Confirm')
        self.do_leave_game.dispatch.bind('click', self.engine.leaveGame)
        self.dont_leave_game = gui.Button(self.leave_game, gui.RelativePos(to=self.do_leave_game,
                                                                           x='right', y='top', padx=5),
                                          'Return to Game')
        self.dont_leave_game.dispatch.bind('click', self.passLeaveGame)

        self.leave_game.visible = False


        self.ui_whos_turn = gui.Label(self.app, (200, 340), 'Players <team> turn')
        self.ui_whos_turn.font = lil_font


        self.select_action = gui.DisableMenu(self.app, (0,0), padding=(2,2))
        self.select_action.entry_bg_color = (200,75,75)
        self.select_action.dispatch.bind('select', self.handle_action_sel)
        self.select_action.visible = False
        self.select_action.bg_color = (100,100,100,255)

        ###game code:

        self.selected_unit = None
        self.selected_action = None
        self.event_handler.dispatch.bind('mouseup', self.handle_mouseup)
        self.event_handler.dispatch.bind('keydown', self.handle_input_key)

        self.lock = False

    def handle_input_submit(self, *args):
        text = self.input_type.text
        if text.startswith('/list'):
            self.messages.add_line('<info>players: '+', '.join([i[0] for i in self.engine.players]))
        elif text.startswith('/kick') and self.engine.am_master:
            self.engine.masterKickPlayer(text.split()[-1])
        elif text:
            self.engine.sendMessage(text)
        self.input_type.text = ''
        self.input_type.cursor_pos = 0
        self.input_cont.visible = False

    def handle_input_key(self, key, name):
        if key == K_RETURN:
            self.input_cont.visible = not self.input_cont.visible

    def handle_action_sel(self, value, disabled):
        if disabled:
            return

        self.selected_action = value
        self.select_action.visible = False
        act = None
        for i in self.selected_unit.actions:
            if i.name == value:
                act = i
                break
        if act:
            self.selected_action = act
            self.selected_action.render_select()
        else:
            'error - non-existant action select <%s>'%act

    def select_unit(self, unit):
        self.selected_unit = unit
        self.gfx.mapd.clear_highlights()
        self.selected_action = None

        if unit:
            self.unit_info_sub.visible = True
            self.ui_icon.image = self.gfx.images.images[unit.image]
            self.ui_name.text = unit.name
            self.ui_hp.text = 'HP: %s/%s'%(unit.cur_hp, unit.hp)
            self.ui_ap.text = 'AP: %s/%s'%(unit.cur_ap, unit.action_points)
            self.ui_strength.text = 'STR: %s'%unit.strength

            self.unit_desc_sub.visible = True
            self.unit_desc2.text = unit.desc
            self.unit_abil2.text = ', '.join([i.name for i in unit.actions])

            self.gfx.camera.set_pos(*unit.pos)

            self.select_action.visible = True
            self.select_action.options = [(i.name, not i.test_available()) for i in unit.actions]
            self.select_action.build_options()

            sx,sy = self.select_action.size
            px, py = 300, 200
            px = min((px, 640-sx))
            py = min((py, 480-sy))
            self.select_action.pos = gui.AbsolutePos((px, py))
            self.select_action.focus()

        else:
            self.unit_info_sub.visible = False
            self.unit_desc_sub.visible = False
            self.select_action.visible = False

    def handle_mouseup(self, button, name):
        sel = None
        if name == 'left':
            xy = self.gfx.mapd.get_mouse_tile()
            if xy:
                if self.selected_action:
                    if self.selected_action.test_acceptable(xy):
                        self.engine.talkToServer("requestAction", (self.selected_unit.gid, self.selected_action.name, xy))
                    self.selected_action = None
                    self.gfx.mapd.clear_highlights()
                    return
                else:
                    for unit in self.mod.units:
                        if unit.pos == xy:
                            sel = unit
                            break

        self.select_unit(sel)
        

    def deactivate_commands(self):
        for x in [self.next_unit, self.end_turn]:
            x.text_color = x.text_reg_color = x.text_hover_color = x.text_click_color = (100,100,100)
            x.bg_color = (0,0,0,0)
    def activate_commands(self):
        if not self.commands_active:
            self.commands_active = True
            for x in [self.next_unit, self.end_turn]:
                x.text_color = (0,0,0)
                x.text_reg_color = (0,0,0)
                x.text_hover_color = (255,0,0)
                x.text_click_color = (255,100,100)
                x.bg_color = (255,255,255)

    def endMyTurn(self, *args):
        if self.engine.whos_turn == self.engine.my_team:
            self.engine.talkToServer('playerEndTurn', None)
            self.deactivate_commands()
            self.select_unit(None)

    def goToNextUnit(self, *args):
        for i in self.mod.units:
            if i == self.selected_unit:
                continue
            if i.cur_ap:
                self.select_unit(i)
                return

        self.select_unit(None)

    def queryLeaveGame(self, *args):
        self.leave_game.visible = True
        self.lock = True
        self.leave_game.focus()
    def passLeaveGame(self, *args):
        self.leave_game.visible = False
        self.lock = False

    def doAction(self, gid, action, target):
        unit = None
        for i in self.mod.units:
            if i.gid == gid:
                unit = i
                break

        act = None
        for i in unit.actions:
            if i.name == action:
                act = i
                break

        if unit and act:
            act.perform(target)

        unit.gfx_entity.pos = unit.pos
        self.select_unit(unit)

    def update(self):
        if self.engine.whos_turn == self.engine.my_team:
            self.activate_commands()

        self.ui_whos_turn.text = 'TURN: Team "%s"' % self.engine.whos_turn
        if self.engine.whos_turn in self.engine.free_teams:
            self.ui_whos_turn.text += " <AI>"

        self.event_handler.update()
        if self.event_handler.quit:
            self.engine.client.engine.close_app() #sheesh!
            return

        if not self.lock:
            mx, my = self.event_handler.mouse.get_pos()
            if mx < 5:
                self.gfx.camera.move(-0.1, 0)
            elif mx > 635:
                self.gfx.camera.move(0.1, 0)

            if my < 5:
                self.gfx.camera.move(0, -0.1)
            elif my > 475:
                self.gfx.camera.move(0, 0.1)

            #TODO: change this
            if not self.selected_unit:
                xy = self.gfx.mapd.get_mouse_tile()
                self.gfx.mapd.clear_highlights()
                if xy:
                    self.gfx.mapd.add_highlight('gui_mouse-hover2.png', xy)

##        if 'left' in self.event_handler.mouse.active:
##            if xy:
##                for unit in self.mod.units:
##                    x,y = unit.pos
##                    if (x,y) == xy:
##                        unit.actions['walk'].render_select()

        self.screen.fill((0,0,0))
        self.gfx.render()
        self.app.render()
        pygame.display.flip()
