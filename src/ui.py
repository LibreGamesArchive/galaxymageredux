import pyggel
from pyggel import *

class MessageBox(pyggel.gui.Frame):
    def __init__(self, app, num_messages=20, **kwargs):
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

    def add_message(self, message):
        x = pyggel.gui.Label(self, message)
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
        self.children = {"chat":ChatWindow}

        self.event_handler = pyggel.event.Handler()
        self.scene = pyggel.scene.Scene()
        self.app = pyggel.gui.App(self.event_handler)
        self.app.theme.load("data/gui/theme.py")
        self.app.packer.packtype="center"
        pyggel.gui.Button(self.app, "Chat!", callbacks=[lambda:self.goto("chat")])
        self.scene.add_2d(self.app)

    def update(self):
        if self.active_child:
            self.active_child.update()
        else:
            self.event_handler.update()
            if self.event_handler.quit:
                self.game.close()
                self.game.running = False
                pyggel.quit()
                return None

            pyggel.view.clear_screen()
            self.scene.render()
            pyggel.view.refresh_screen()

class ChatWindow(GameState):
    def __init__(self, game, parent=None):
        GameState.__init__(self, game, parent)
        self.event_handler = pyggel.event.Handler()
        self.scene = pyggel.scene.Scene()
        self.app = pyggel.gui.App(self.event_handler)
        self.app.theme.load("data/gui/theme.py")
        self.message_frame = MessageBox(self.app, size=(630, 400)) #640-10 for tile size
        pyggel.gui.NewLine(self.app)
        self.input = pyggel.gui.Input(self.app, callback=self.send_netMessage, font_color=(1,1,1,1),
                                      width=630)
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
        self.message_frame.add_message(message) #TODO: color red