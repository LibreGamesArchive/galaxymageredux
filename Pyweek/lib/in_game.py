import gfx_engine, gui, mod_base

class Game(object):
    def __init__(self, engine):
        self.engine = engine

        self.gfx = gfx_engine.GFXEngine(engine.client.screen, engine.scenario)
        self.mod = mod_base.Scenario(engine.scenario)

        self.event_handler = engine.client.event_handler

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
