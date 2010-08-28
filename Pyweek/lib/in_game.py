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
        self.input_cont.bg_color = (100,100,255,100)
        self.input_type = gui.Input(self.input_cont, 225, (5,5))
        self.input_type.bg_color = (0,0,0,0)
        self.input_butt = gui.Button(self.input_cont,
                                     gui.RelativePos(to=self.input_type, x='right', y='top', padx=5),
                                     'Submit')
        self.input_butt.bg_color = (150,150,255,100)

        self.input_cont.visible = False
        self.event_handler.dispatch.bind('keydown', self.handle_input_key)
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

        self.unit_desc = gui.Container(self.app, (320, 100), (160, 375))
        self.unit_desc.bg_color = (100,100,255,100)
        self.unit_desc.font = lil_font

        ###game code:

        self.selected_unit = None
        self.event_handler.dispatch.bind('mousedown', self.try_select_unit)

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

    def select_unit(self, unit):
        self.selected_unit = unit

        if unit:
            self.unit_info_sub.visible = True
            self.ui_icon.image = self.gfx.images.images[unit.image]
            self.ui_name.text = unit.name
            self.ui_hp.text = 'HP: %s/%s'%(unit.cur_hp, unit.hp)
            self.ui_ap.text = 'AP: %s/%s'%(unit.cur_ap, unit.action_points)
            self.ui_strength.text = 'STR: %s'%unit.strength
        else:
            self.unit_info_sub.visible = False

    def try_select_unit(self, button, name):
        sel = None
        if name == 'left':
            xy = self.gfx.mapd.get_mouse_tile()
            if xy:
                for unit in self.mod.units:
                    if unit.pos == xy:
                        sel = unit
                        break

        self.select_unit(sel)

    def update(self):
##        if self.engine.whos_turn == self.engine.my_team:
##            print 'my turn', self.engine.my_team
##            self.engine.talkToServer('playerEndTurn', None)
##        elif self.engine.whos_turn in self.engine.free_teams:
##            #AI player
##            print 'AI turn', self.engine.whos_turn
##            self.engine.talkToServer('playerEndTurn', None)
##        else:
##            print 'his turn', self.engine.whos_turn

        self.event_handler.update()
        if self.event_handler.quit:
            self.engine.client.engine.close_app() #sheesh!
            return

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
