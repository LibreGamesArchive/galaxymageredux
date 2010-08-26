import gfx_engine, gui, mod_base

class Game(object):
    def __init__(self, engine):
        self.engine = engine

        self.gfx = gfx_engine.GFXEngine(engine.client.screen, engine.scenario)
        self.mod = mod_base.Scenario(engine.scenario)

        self.event_handler = engine.client.event_handler

        self.app = gui.App(engine.client.screen,
                           engine.client.event_handler)

        self.messages = gui.MessageBox(self.app,
                                       (630, 50),
                                       (5,5))
        self.messages.max_lines = 5
        self.messages.bg_color = (0,0,0,0)
        self.messages.entry_bg_color = (100,100,255,100)

    def update(self):
        mx, my = self.event_handler.mouse.get_pos()
        if mx < 5:
            self.gfx.camera.move(-0.1, 0)
        elif mx > 635:
            self.gfx.camera.move(0.1, 0)

        if my < 5:
            self.gfx.camera.move(0, -0.1)
        elif my > 475:
            self.gfx.camera.move(0, 0.1)

        self.gfx.render()
