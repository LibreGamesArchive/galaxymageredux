import gfx_engine, gui, mod_base, event
import pygame
from pygame.locals import *

class Game(object):
    def __init__(self, engine):
        self.engine = engine
        self.screen = engine.client.screen

        self.gfx = gfx_engine.GFXEngine(engine.client.screen, engine.scenario)
        self.mod = mod_base.Scenario(engine.scenario)

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

        self.input_cont = gui.Container(self.app, (630, 30), (5, 445))
        self.input_cont.bg_color = (100,100,255,100)
        self.input_type = gui.Input(self.input_cont, 300, (5,5))
        self.input_type.bg_color = (0,0,0,0)
        self.input_butt = gui.Button(self.input_cont,
                                     gui.RelativePos(to=self.input_type, x='right', y='top', padx=150),
                                     'Submit')
        self.input_butt.bg_color = (150,150,255,100)

        self.input_cont.visible = False
        self.event_handler.dispatch.bind('keydown', self.handle_input_key)
        self.input_type.dispatch.bind('input-submit', self.handle_input_submit)
        self.input_butt.dispatch.bind('click', self.handle_input_submit)

    def handle_input_submit(self, *args):
        text = self.input_type.text
        if text:
            self.engine.sendMessage(text)
            self.input_type.text = ''
            self.input_type.cursor_pos = 0
        self.input_cont.visible = False

    def handle_input_key(self, key, name):
        if key == K_RETURN:
            self.input_cont.visible = not self.input_cont.visible

    def update(self):

        self.event_handler.update()
        if self.event_handler.quit:
            self.engine.client.close_app()
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

        self.screen.fill((0,0,0))
        self.gfx.render()
        self.app.render()
        pygame.display.flip()
