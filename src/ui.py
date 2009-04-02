import pyggel
from pyggel import *

import objects

class MessageBox(pyggel.gui.Frame):
    def __init__(self, app, num_messages=15, **kwargs):
        pyggel.gui.Frame.__init__(self, app, **kwargs)
        self.num_messages = num_messages

        self.theme = pyggel.gui.Theme(self)
        self.theme.load("data/gui/theme.py")
        l = self.theme.theme["Label"]
        l["background-image"] = None

        self.packer.pack_upwards = self.pack_upwards
        self.packer.packtype = "upwards"
        self._messages = []

    def pack_upwards(self):
        bottom = self.size[1]-self.tsize[1]*2
        self.widgets.reverse() #flip them!
        for i in self.widgets:
            pos = (0, bottom-i.size[1])
            bottom -= i.size[1]
            i.force_pos_update(pos)
        self.widgets.reverse()

    def add_message(self, message, color=(1,1,1,1)):
        x = pyggel.gui.Label(self, message, font_color=color, font_color_inactive=color)
        self._messages.append(x)
        if len(self.widgets) > self.num_messages:
            x = self._messages[0]
            self.widgets.remove(x)
            self._messages.remove(x)

class GameState(object):
    def __init__(self, game, parent=None):
        self.game = game
        self.parent = parent
        self.children = {}

        self.active_child = None

    def goback(self):
        if self.parent:
            self.parent.active_child = None

    def goto(self, child_name):
        self.active_child = self.children[child_name](self.game, self)

    def update(self):
        if self.active_child:
            self.active_child.update()

    def get_netMessage(self, message):
        if self.active_child:
            self.active_child.get_netMessage(message)

    def get_errorMessage(self, message):
        if self.active_child:
            self.active_child.get_errorMessage(message)

    def send_netMessage(self, message):
        self.game.sendMessage(message)

class MainMenu(GameState):
    def __init__(self, game, parent=None):
        GameState.__init__(self, game)
        self.children = {"chat":ChatWindow,
                         "test_map":TestMap}

        self.event_handler = pyggel.event.Handler()
        self.scene = pyggel.scene.Scene()
        self.app = pyggel.gui.App(self.event_handler)
        self.app.theme.load("data/gui/theme.py")
        self.app.packer.packtype="center"
        self.settings_app = pyggel.gui.App(self.event_handler)
        self.settings_app.theme = self.app.theme
        self.settings_app.packer.packtype="center"

        frame = pyggel.gui.Frame(self.settings_app, size=(400,200))
        #TODO: add widgets to swap back!!!
        self.checks = pyggel.gui.MultiChoiceRadio(frame, options=["FPS",
                                                                  "sound",
                                                                  "fullscreen",
                                                                  "verbose_logging"])
        for i in self.checks.options:
            name, check, label, state = i
            state = int(self.game.config[name])
            check.state = state
            i[0], i[1], i[2], i[3] = name, check, label, state
        self.resolution = pyggel.gui.Radio(frame, options=["640x480",
                                                           "800x600",
                                                           "1024x768",
                                                           "1680x1050"])
        x = "%sx%s"%self.game.config["resolution"]
        if x in self.resolution.states:
            for i in self.resolution.options:
                name, check, label, state = i
                if name == x:
                    state = 1
                    check.state = 1
                else:
                    state = 0
                    check.state = 0
                i[0], i[1], i[2], i[3] = name, check, label, state
        else:
            pass

        pyggel.gui.NewLine(frame)
        pyggel.gui.Button(frame, "Save Changes", callbacks=[self.save_options])
        pyggel.gui.Button(frame, "Back", callbacks=[self.app.activate])
        self.scene.add_2d(self.settings_app)
        self.app.activate()

        pyggel.gui.Button(self.app, "Single Player", callbacks=[lambda:self.goto("test_map")])
        pyggel.gui.NewLine(self.app)
        pyggel.gui.Button(self.app, "Multiplayer", callbacks=[lambda:self.goto("chat")])
        pyggel.gui.NewLine(self.app)
        pyggel.gui.Button(self.app, "Options", callbacks=[self.settings_app.activate])
        pyggel.gui.NewLine(self.app)
        pyggel.gui.Button(self.app, "Exit", callbacks=[self.force_quit])
        self.scene.add_2d(self.app)

    def get_option_resolution(self):
        r = "640x480"
        for i in self.resolution.states:
            if self.resolution.states[i]: r = i
        a, b = r.split("x")
        return (int(a), int(b))

    def save_options(self):
        fobj = open("data/config.txt", "w")
        fobj.write("name='reduxian'\nFPS=%s\nsound=%s\nfullscreen=%s\nverbose_logging=%s\nresolution=%s"%(
            bool(self.checks.states["FPS"]),
            bool(self.checks.states["sound"]),
            bool(self.checks.states["fullscreen"]),
            bool(self.checks.states["verbose_logging"]),
            self.get_option_resolution()))
        fobj.close()

    def force_quit(self):
        self.event_handler.quit = True

    def update(self):
        if self.active_child:
            self.active_child.update()
        else:
            self.event_handler.update()
            if self.event_handler.quit:
                self.exit()
                return None
            pyggel.view.clear_screen()
            self.scene.render()
            pyggel.view.refresh_screen()

    def exit(self):
        self.game.close()
        self.game.running = False
        pyggel.quit()

class ChatWindow(GameState):
    def __init__(self, game, parent=None):
        GameState.__init__(self, game, parent)
        self.event_handler = pyggel.event.Handler()
        self.scene = pyggel.scene.Scene()
        self.app = pyggel.gui.App(self.event_handler)
        self.app.theme.load("data/gui/theme.py")
        self.message_frame = MessageBox(self.app, size=(200, 200))
        pyggel.gui.NewLine(self.app)
        self.input = pyggel.gui.Input(self.app, callback=self.send_netMessage, font_color=(1,1,1,1),
                                      width=200)
        pyggel.gui.NewLine(self.app)
        pyggel.gui.Button(self.app, "Menu", callbacks=[self.stop])
        self.scene.add_2d(self.app)
        self.game.connect()

    def stop(self):
        self.goback()
        self.game.disconnect()

    def update(self):
        GameState.update(self)
        if not self.input.key_active:
            self.input.key_active = True #make sure the input always takes, well, input...

        self.event_handler.update()
        if self.event_handler.quit:
            self.game.close()
            self.game.running = False
            pyggel.quit()
            return None

        pyggel.view.clear_screen()
        self.scene.render()
        pyggel.view.refresh_screen()

    def get_netMessage(self, message):
        GameState.get_netMessage(self, message)
        self.message_frame.add_message(message)
    
    def get_errorMessage(self, message):
        GameState.get_netMessage(self, message)
        self.message_frame.add_message(message, color=(1,.1,.1,1))

class TestMap(GameState):
    def __init__(self, game, parent=None):
        GameState.__init__(self, game, parent)

        self.event_handler = pyggel.event.Handler()
        self.scene = pyggel.scene.Scene()
        self.app = pyggel.gui.App(self.event_handler)
        self.app.theme.load("data/gui/theme.py")
        pyggel.gui.Button(self.app, "Menu", callbacks=[self.goback])
        self.scene.add_2d(self.app)

        tiles = objects.parse_map("data/core/map/test_map.py")
        self.scene.add_3d(tiles)

        self.camera = pyggel.camera.LookAtCamera((0,0,0), distance=15)

        light = pyggel.light.Light((2,100,2), (1,1,1,1),
                                  (1,1,1,1), (50,50,50,50),
                                  (0,0,0), True)
        self.scene.add_light(light)

        _image = pyggel.image.Image3D("data/core/image/unit_example.png")

        self.unit = objects.Unit(tiles[1],#lets see how that works ;)
                                 pos=(0,0),
                                 image=_image, colorize=(1,1,1,1))
        self.scene.add_3d(self.unit)

    def update(self):
        GameState.update(self)

        self.event_handler.update()
        if self.event_handler.quit:
            self.game.close()
            self.game.running = False
            pyggel.quit()
            return None

        if K_LEFT in self.event_handler.keyboard.active:
            self.camera.roty -= 1
        if K_RIGHT in self.event_handler.keyboard.active:
            self.camera.roty += 1
        if K_UP in self.event_handler.keyboard.active:
            self.camera.rotx -= 1
        if K_DOWN in self.event_handler.keyboard.active:
            self.camera.rotx += 1

        pyggel.view.clear_screen()
        touching = self.scene.pick(pyggel.view.screen.get_mouse_pos(), self.camera)
        if isinstance(touching, objects.Unit):
            touching = touching.tile
        if touching:
            _col = touching.colorize
            touching.colorize = (1,0,0,1)
        if "left" in self.event_handler.mouse.hit:
            if isinstance(touching, objects.Tile):
                self.unit.tile = touching
        self.scene.render(self.camera)
        if touching:
            touching.colorize = _col
        pyggel.view.refresh_screen()
